"""
Module de nettoyage et complétion des données ENEDIS
"""
from datetime import datetime, timedelta
import pandas as pd

class DataCleaner:
    """Classe pour nettoyer et compléter les données manquantes"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialise le nettoyeur de données
        
        Args:
            data: DataFrame contenant les données ENEDIS
        """
        self.data = data.copy()
        if 'Source' not in self.data.columns:
            self.data['Source'] = 'original'
    
    def detect_missing_hours(self, year: str) -> list:
        """
        Détecte les heures manquantes pour une année donnée
        
        Args:
            year: Année à vérifier (str)
            
        Returns:
            Liste des datetimes manquants
        """
        # Filtre les données pour l'année
        year_data = self.get_data_by_year(year)
        
        if year_data.empty:
            return []
        
        # Utilise la plage de dates existante
        start_date = year_data['Horodate'].min()
        end_date = year_data['Horodate'].max()
        expected_dates = pd.date_range(start=start_date, end=end_date, freq='H')
        
        # Trouve les dates manquantes
        missing_dates = expected_dates[~expected_dates.isin(year_data['Horodate'])]
        return list(missing_dates)
    
    def find_replacement_data(self, missing_dt: datetime) -> float:
        """
        Cherche une donnée de remplacement pour une date/heure manquante
        
        Args:
            missing_dt: Date et heure manquante
            
        Returns:
            Valeur de remplacement ou None si non trouvée
        """
        # Cherche d'abord dans l'année suivante
        next_year = missing_dt.year + 1
        next_year_dt = missing_dt.replace(year=next_year)
        replacement = self.data[self.data['Horodate'] == next_year_dt]
        
        if not replacement.empty:
            return replacement.iloc[0]['Valeur']
            
        # Si non trouvé, cherche dans l'année précédente
        prev_year = missing_dt.year - 1
        prev_year_dt = missing_dt.replace(year=prev_year)
        replacement = self.data[self.data['Horodate'] == prev_year_dt]
        
        if not replacement.empty:
            return replacement.iloc[0]['Valeur']
            
        return None
    
    def fill_missing_data(self, year: str) -> pd.DataFrame:
        """
        Remplit les données manquantes pour une année
        
        Args:
            year: Année à compléter
            
        Returns:
            DataFrame avec les données complétées
        """
        missing_hours = self.detect_missing_hours(year)
        df = self.data.copy()
        
        for missing_dt in missing_hours:
            replacement_value = self.find_replacement_data(missing_dt)
            if replacement_value is not None:
                # Ajoute la nouvelle ligne avec la donnée de remplacement
                new_row = pd.DataFrame({
                    'Horodate': [missing_dt],
                    'Valeur': [replacement_value],
                    'Source': [str(missing_dt.year + 1)]  # Source = année utilisée
                })
                df = pd.concat([df, new_row], ignore_index=True)
        
        return df.sort_values('Horodate').reset_index(drop=True)
    
    def get_data_by_year(self, year: str) -> pd.DataFrame:
        """
        Extrait les données pour une année spécifique
        
        Args:
            year: Année à extraire
            
        Returns:
            DataFrame filtré pour l'année
        """
        return self.data[self.data['Horodate'].dt.year == int(year)]
