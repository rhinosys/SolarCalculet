"""
Module principal pour le nettoyage des données ENEDIS.
"""
import os
from typing import Dict, List
from datetime import datetime, timedelta
import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv

class DataCleaner:
    def __init__(self):
        """Initialise le nettoyeur de données."""
        load_dotenv()
        self.mongo_uri = os.getenv('MONGODB_URI')
        self.db_name = os.getenv('MONGODB_DB')
        self.collection_name = os.getenv('MONGODB_COLLECTION')
        self.client = None
        self.db = None
        
    def connect_to_mongodb(self) -> bool:
        """Établit la connexion à MongoDB.
        
        Returns:
            bool: True si la connexion est réussie, False sinon.
        """
        try:
            self.client = MongoClient(self.mongo_uri)
            self.db = self.client[self.db_name]
            return True
        except Exception as e:
            print(f"Erreur de connexion à MongoDB: {e}")
            return False
            
    def read_csv_file(self, file_path: str) -> pd.DataFrame:
        """Lit le fichier CSV des données ENEDIS.
        
        Args:
            file_path: Chemin vers le fichier CSV.
            
        Returns:
            DataFrame contenant les données.
        """
        try:
            df = pd.read_csv(file_path, sep=';', parse_dates=['Horodate'])
            return df
        except Exception as e:
            print(f"Erreur lors de la lecture du fichier CSV: {e}")
            raise
            
    def validate_data_format(self, df: pd.DataFrame) -> Dict[str, List[int]]:
        """Valide le format des données et identifie les problèmes.
        
        Args:
            df: DataFrame à valider.
            
        Returns:
            Dict contenant les indices des lignes problématiques.
        """
        validation_result = {
            'invalid_rows': [],
            'missing_values': []
        }
        
        # Vérifie les valeurs manquantes
        missing_mask = df['Consommation (Wh)'].isna()
        validation_result['missing_values'] = missing_mask[missing_mask].index.tolist()
        
        # Vérifie les valeurs invalides (non numériques)
        for idx, value in df['Consommation (Wh)'].items():
            if pd.notna(value) and not str(value).replace('.', '').isdigit():
                validation_result['invalid_rows'].append(idx)
                
        return validation_result
        
    def detect_missing_hours(self, df: pd.DataFrame, date: str) -> List[str]:
        """Détecte les heures manquantes pour une date donnée.
        
        Args:
            df: DataFrame des données.
            date: Date à vérifier au format 'YYYY-MM-DD'.
            
        Returns:
            Liste des heures manquantes au format 'YYYY-MM-DD HH:00:00'.
        """
        # Crée une liste de toutes les heures possibles pour la date
        start_date = datetime.strptime(date, '%Y-%m-%d')
        all_hours = [(start_date + timedelta(hours=i)).strftime('%Y-%m-%d %H:%M:%S') 
                     for i in range(24)]
        
        # Filtre les heures présentes dans le DataFrame
        df_date = df[df['Horodate'].dt.date == start_date.date()]
        present_hours = df_date['Horodate'].dt.strftime('%Y-%m-%d %H:%M:%S').tolist()
        
        # Trouve les heures manquantes
        missing_hours = [hour for hour in all_hours if hour not in present_hours]
        
        return missing_hours
        
    def find_replacement_data(self, df: pd.DataFrame, timestamp: str) -> float:
        """Trouve une valeur de remplacement pour une heure donnée.
        
        Args:
            df: DataFrame des données.
            timestamp: Horodate au format 'YYYY-MM-DD HH:MM:SS'.
            
        Returns:
            Valeur de consommation de remplacement ou None si aucune trouvée.
        """
        dt = datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        hour = dt.hour
        
        # Cherche d'abord dans 2024
        replacement_2024 = df[
            (df['Horodate'].dt.year == 2024) &
            (df['Horodate'].dt.hour == hour) &
            df['Consommation (Wh)'].notna()
        ]['Consommation (Wh)'].iloc[0] if len(df[
            (df['Horodate'].dt.year == 2024) &
            (df['Horodate'].dt.hour == hour) &
            df['Consommation (Wh)'].notna()
        ]) > 0 else None
        
        if replacement_2024 is not None:
            return float(replacement_2024)
            
        # Sinon cherche dans 2025
        replacement_2025 = df[
            (df['Horodate'].dt.year == 2025) &
            (df['Horodate'].dt.hour == hour) &
            df['Consommation (Wh)'].notna()
        ]['Consommation (Wh)'].iloc[0] if len(df[
            (df['Horodate'].dt.year == 2025) &
            (df['Horodate'].dt.hour == hour) &
            df['Consommation (Wh)'].notna()
        ]) > 0 else None
        
        if replacement_2025 is not None:
            return float(replacement_2025)
            
        # Si aucune valeur trouvée, retourne None
        return None
        
    def complete_missing_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Complète les données manquantes dans le DataFrame.
        
        Args:
            df: DataFrame à compléter.
            
        Returns:
            DataFrame avec les données complétées.
        """
        df_copy = df.copy()
        
        # Identifie les lignes avec des données manquantes
        missing_mask = df_copy['Consommation (Wh)'].isna()
        missing_rows = df_copy[missing_mask]
        
        # Pour chaque ligne manquante
        for idx, row in missing_rows.iterrows():
            timestamp = row['Horodate'].strftime('%Y-%m-%d %H:%M:%S')
            replacement = self.find_replacement_data(df, timestamp)
            
            if replacement is not None:
                df_copy.at[idx, 'Consommation (Wh)'] = replacement
        
        return df_copy
        
    def validate_completed_data(self, df: pd.DataFrame) -> Dict[str, any]:
        """Valide les données complétées.
        
        Args:
            df: DataFrame à valider.
            
        Returns:
            Dict avec le résultat de la validation.
        """
        validation_result = {
            'is_valid': True,
            'errors': []
        }
        
        # Vérifie s'il reste des valeurs manquantes
        missing_values = df['Consommation (Wh)'].isna().sum()
        if missing_values > 0:
            validation_result['is_valid'] = False
            validation_result['errors'].append(
                f'Il reste {missing_values} valeurs manquantes'
            )
        
        # Vérifie que toutes les valeurs sont numériques
        non_numeric = df['Consommation (Wh)'].apply(
            lambda x: not str(x).replace('.', '').isdigit() if pd.notna(x) else False
        ).sum()
        if non_numeric > 0:
            validation_result['is_valid'] = False
            validation_result['errors'].append(
                f'Il y a {non_numeric} valeurs non numériques'
            )
        
        return validation_result
        
    def store_data_in_mongodb(self, df: pd.DataFrame) -> bool:
        """Stocke les données dans MongoDB.
        
        Args:
            df: DataFrame à stocker.
            
        Returns:
            bool: True si le stockage est réussi, False sinon.
        """
        try:
            # Convertit le DataFrame en format JSON
            data = df.to_dict('records')
            
            # Supprime les anciennes données
            self.db[self.collection_name].delete_many({})
            
            # Insère les nouvelles données
            self.db[self.collection_name].insert_many(data)
            
            return True
        except Exception as e:
            print(f"Erreur lors du stockage dans MongoDB: {e}")
            return False
            
    def organize_data_by_year(self, df: pd.DataFrame) -> Dict[int, pd.DataFrame]:
        """Organise les données par année.
        
        Args:
            df: DataFrame à organiser.
            
        Returns:
            Dict avec les DataFrames par année.
        """
        data_by_year = {}
        
        # Groupe les données par année
        for year in [2023, 2024, 2025]:
            year_data = df[df['Horodate'].dt.year == year].copy()
            if not year_data.empty:
                data_by_year[year] = year_data
        
        return data_by_year
        
    def generate_output_files(self, df: pd.DataFrame, output_dir: str) -> bool:
        """Génère les fichiers de sortie par année.
        
        Args:
            df: DataFrame avec les données.
            output_dir: Répertoire de sortie.
            
        Returns:
            bool: True si la génération est réussie, False sinon.
        """
        try:
            # Organise les données par année
            data_by_year = self.organize_data_by_year(df)
            
            # Génère les fichiers pour 2023 et 2024
            for year in [2023, 2024]:
                if year in data_by_year:
                    output_file = os.path.join(output_dir, f'{year}.csv')
                    data_by_year[year].to_csv(output_file, sep=';', index=False)
            
            return True
        except Exception as e:
            print(f"Erreur lors de la génération des fichiers: {e}")
            return False
