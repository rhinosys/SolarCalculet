"""
Tests pour le module data_cleaner.
"""
import os
import pytest
import pandas as pd
from src.data_cleaner import DataCleaner

def test_data_cleaner_initialization():
    """Test l'initialisation du DataCleaner."""
    cleaner = DataCleaner()
    assert cleaner is not None
    assert cleaner.mongo_uri is not None
    assert cleaner.db_name is not None
    assert cleaner.collection_name is not None

def test_mongodb_connection():
    """Test la connexion à MongoDB."""
    cleaner = DataCleaner()
    assert cleaner.connect_to_mongodb() is True
    assert cleaner.client is not None
    assert cleaner.db is not None

def test_read_csv_file(test_data_dir):
    """Test la lecture du fichier CSV."""
    cleaner = DataCleaner()
    file_path = os.path.join(test_data_dir, 'sample.csv')
    df = cleaner.read_csv_file(file_path)
    assert isinstance(df, pd.DataFrame)
    assert len(df) == 6
    assert all(col in df.columns for col in ['Horodate', 'Consommation (Wh)'])

def test_validate_data_format(test_data_dir):
    """Test la validation du format des données."""
    cleaner = DataCleaner()
    file_path = os.path.join(test_data_dir, 'sample.csv')
    df = cleaner.read_csv_file(file_path)
    validation_result = cleaner.validate_data_format(df)
    assert isinstance(validation_result, dict)
    assert 'invalid_rows' in validation_result
    assert 'missing_values' in validation_result
    assert len(validation_result['invalid_rows']) == 1  # Une ligne avec 'invalid'
    assert len(validation_result['missing_values']) == 1  # Une ligne avec valeur manquante

def test_detect_missing_hours(test_data_dir):
    """Test la détection des heures manquantes."""
    cleaner = DataCleaner()
    file_path = os.path.join(test_data_dir, 'sample.csv')
    df = cleaner.read_csv_file(file_path)
    missing_hours = cleaner.detect_missing_hours(df, '2023-01-01')
    assert isinstance(missing_hours, list)
    assert len(missing_hours) == 19  # 24 heures - 5 heures présentes pour 2023-01-01

def test_find_replacement_data(test_data_dir):
    """Test la recherche des données de remplacement."""
    cleaner = DataCleaner()
    file_path = os.path.join(test_data_dir, 'full_sample.csv')
    df = cleaner.read_csv_file(file_path)
    
    # Test pour une heure spécifique
    replacement = cleaner.find_replacement_data(df, '2023-01-01 02:00:00')
    assert replacement is not None
    assert isinstance(replacement, float)
    assert replacement in [140, 155]  # Valeur de 2024 ou 2025

def test_complete_missing_data(test_data_dir):
    """Test le remplacement des données manquantes."""
    cleaner = DataCleaner()
    file_path = os.path.join(test_data_dir, 'full_sample.csv')
    df = cleaner.read_csv_file(file_path)
    
    # Compte les valeurs manquantes avant
    missing_before = df['Consommation (Wh)'].isna().sum()
    assert missing_before > 0
    
    # Complète les données
    df_completed = cleaner.complete_missing_data(df)
    
    # Vérifie qu'il n'y a plus de données manquantes
    missing_after = df_completed['Consommation (Wh)'].isna().sum()
    assert missing_after == 0
    
    # Vérifie que les valeurs remplacées sont cohérentes
    assert all(df_completed['Consommation (Wh)'].notna())
    assert all(df_completed['Consommation (Wh)'].astype(str).str.replace('.', '').str.isdigit())

def test_validate_completed_data(test_data_dir):
    """Test la validation des données complétées."""
    cleaner = DataCleaner()
    file_path = os.path.join(test_data_dir, 'full_sample.csv')
    df = cleaner.read_csv_file(file_path)
    
    # Complète les données
    df_completed = cleaner.complete_missing_data(df)
    
    # Valide les données complétées
    validation_result = cleaner.validate_completed_data(df_completed)
    assert validation_result['is_valid'] is True
    assert len(validation_result['errors']) == 0

def test_store_data_in_mongodb(test_data_dir):
    """Test le stockage des données dans MongoDB."""
    cleaner = DataCleaner()
    cleaner.connect_to_mongodb()
    
    # Charge et prépare les données
    file_path = os.path.join(test_data_dir, 'full_sample.csv')
    df = cleaner.read_csv_file(file_path)
    df_completed = cleaner.complete_missing_data(df)
    
    # Stocke les données
    result = cleaner.store_data_in_mongodb(df_completed)
    assert result is True
    
    # Vérifie que les données sont bien stockées
    data_count = cleaner.db[cleaner.collection_name].count_documents({})
    assert data_count > 0

def test_organize_data_by_year(test_data_dir):
    """Test l'organisation des données par année."""
    cleaner = DataCleaner()
    file_path = os.path.join(test_data_dir, 'full_sample.csv')
    df = cleaner.read_csv_file(file_path)
    df_completed = cleaner.complete_missing_data(df)
    
    # Organise les données par année
    data_by_year = cleaner.organize_data_by_year(df_completed)
    
    # Vérifie la structure des données
    assert isinstance(data_by_year, dict)
    assert all(year in data_by_year for year in [2023, 2024, 2025])
    assert all(isinstance(data_by_year[year], pd.DataFrame) for year in data_by_year)

def test_generate_output_files(test_data_dir, tmp_path):
    """Test la génération des fichiers de sortie."""
    cleaner = DataCleaner()
    file_path = os.path.join(test_data_dir, 'full_sample.csv')
    df = cleaner.read_csv_file(file_path)
    df_completed = cleaner.complete_missing_data(df)
    
    # Génère les fichiers
    output_dir = str(tmp_path)
    result = cleaner.generate_output_files(df_completed, output_dir)
    assert result is True
    
    # Vérifie que les fichiers existent
    assert os.path.exists(os.path.join(output_dir, '2023.csv'))
    assert os.path.join(output_dir, '2024.csv')
