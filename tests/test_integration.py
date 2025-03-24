"""
Tests d'intégration pour le processus complet de nettoyage des données.
"""
import os
import pandas as pd
import pytest
from src.data_cleaner import DataCleaner

def test_end_to_end_process(test_data_dir, tmp_path):
    """Test le processus complet de bout en bout."""
    # 1. Initialisation
    cleaner = DataCleaner()
    assert cleaner.connect_to_mongodb() is True
    
    # 2. Lecture des données
    input_file = os.path.join(test_data_dir, 'integration_data.csv')
    df = cleaner.read_csv_file(input_file)
    assert isinstance(df, pd.DataFrame)
    assert len(df) > 0
    
    # 3. Validation initiale
    validation = cleaner.validate_data_format(df)
    assert 'invalid_rows' in validation
    assert 'missing_values' in validation
    assert len(validation['invalid_rows']) > 0 or len(validation['missing_values']) > 0
    
    # 4. Complétion des données
    df_completed = cleaner.complete_missing_data(df)
    
    # Supprime les lignes invalides avant la validation finale
    df_completed = df_completed[df_completed['Consommation (Wh)'].apply(
        lambda x: str(x).replace('.', '').isdigit() if pd.notna(x) else False
    )]
    
    validation_completed = cleaner.validate_completed_data(df_completed)
    assert validation_completed['is_valid'] is True
    assert len(validation_completed['errors']) == 0
    
    # 5. Stockage MongoDB
    assert cleaner.store_data_in_mongodb(df_completed) is True
    
    # 6. Organisation par année
    data_by_year = cleaner.organize_data_by_year(df_completed)
    assert 2023 in data_by_year
    assert 2024 in data_by_year
    
    # 7. Génération des fichiers
    output_dir = str(tmp_path)
    assert cleaner.generate_output_files(df_completed, output_dir) is True
    
    # 8. Vérification des fichiers générés
    for year in [2023, 2024]:
        output_file = os.path.join(output_dir, f'{year}.csv')
        assert os.path.exists(output_file)
        df_output = pd.read_csv(output_file, sep=';', parse_dates=['Horodate'])
        assert len(df_output) > 0
        assert all(df_output['Consommation (Wh)'].notna())
        assert all(df_output['Horodate'].dt.year == year)

def test_data_consistency(test_data_dir, tmp_path):
    """Test la cohérence des données entre les fichiers d'entrée et de sortie."""
    cleaner = DataCleaner()
    cleaner.connect_to_mongodb()
    
    # Lecture et traitement
    input_file = os.path.join(test_data_dir, 'integration_data.csv')
    df = cleaner.read_csv_file(input_file)
    df_completed = cleaner.complete_missing_data(df)
    
    # Supprime les lignes invalides
    df_completed = df_completed[df_completed['Consommation (Wh)'].apply(
        lambda x: str(x).replace('.', '').isdigit() if pd.notna(x) else False
    )]
    
    # Génération des fichiers
    output_dir = str(tmp_path)
    cleaner.generate_output_files(df_completed, output_dir)
    
    # Vérification de la cohérence
    total_rows = 0
    for year in [2023, 2024]:
        output_file = os.path.join(output_dir, f'{year}.csv')
        df_output = pd.read_csv(output_file, sep=';', parse_dates=['Horodate'])
        
        # Vérifie que les données valides d'origine sont préservées
        df_year = df[df['Horodate'].dt.year == year]
        valid_data = df_year[df_year['Consommation (Wh)'].notna() & 
                            df_year['Consommation (Wh)'].astype(str).str.replace('.', '').str.isdigit()]
        
        for _, row in valid_data.iterrows():
            matching_rows = df_output[
                (df_output['Horodate'] == row['Horodate']) & 
                (df_output['Consommation (Wh)'].astype(float) == float(row['Consommation (Wh)']))
            ]
            assert len(matching_rows) > 0, f"Donnée manquante pour {row['Horodate']}"
        
        total_rows += len(df_output)
    
    # Vérifie que nous avons des données pour chaque année
    assert total_rows > 0, "Aucune donnée générée"
