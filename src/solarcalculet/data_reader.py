"""
Module de lecture et validation des données ENEDIS
"""
from pathlib import Path
import pandas as pd

class DataReader:
    """Classe pour lire et valider les données ENEDIS"""
    
    REQUIRED_COLUMNS = ["Horodate", "Valeur"]
    
    def __init__(self, file_path: str):
        """
        Initialise le lecteur de données
        
        Args:
            file_path: Chemin vers le fichier CSV ENEDIS
        """
        self.file_path = Path(file_path)
    
    def read(self) -> pd.DataFrame:
        """
        Lit le fichier CSV ENEDIS
        
        Returns:
            DataFrame contenant les données
        """
        df = pd.read_csv(self.file_path, sep=';')
        if 'Horodate' in df.columns:
            df['Horodate'] = pd.to_datetime(df['Horodate'])
        return df
    
    def validate_columns(self, df: pd.DataFrame) -> list:
        """
        Vérifie la présence des colonnes requises
        
        Args:
            df: DataFrame à valider
            
        Returns:
            Liste des colonnes manquantes
        """
        missing = []
        for col in self.REQUIRED_COLUMNS:
            if col not in df.columns:
                missing.append(col)
        return missing
    
    def convert_to_kw(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Convertit les valeurs de W en kW
        
        Args:
            df: DataFrame avec les valeurs en W
            
        Returns:
            DataFrame avec les valeurs en kW
        """
        df = df.copy()
        df["Valeur"] = df["Valeur"] / 1000
        return df
