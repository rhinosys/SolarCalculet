"""
Tests pour le module d'export Excel
"""
import pytest
import pandas as pd
import os
from datetime import datetime
from solarcalculet.excel_exporter import ExcelExporter

@pytest.fixture
def sample_data():
    """Crée un DataFrame de test"""
    data = {
        'Horodate': [
            '2023-01-01 00:00:00',
            '2023-01-01 01:00:00',
            '2023-01-01 02:00:00',
            '2023-12-31 23:00:00'
        ],
        'Valeur': [0.5, 0.6, 0.7, 0.8]
    }
    df = pd.DataFrame(data)
    df['Horodate'] = pd.to_datetime(df['Horodate'])
    return df

def test_format_date_hour(sample_data):
    """Teste le formatage des dates et heures"""
    exporter = ExcelExporter(sample_data)
    formatted = exporter.format_date_hour()
    
    assert 'Month/Day Hour:Minute' in formatted.columns
    assert formatted.iloc[0]['Month/Day Hour:Minute'] == '1/1 0:00'
    assert formatted.iloc[1]['Month/Day Hour:Minute'] == '1/1 1:00'

def test_prepare_excel_data(sample_data):
    """Teste la préparation des données pour Excel"""
    exporter = ExcelExporter(sample_data)
    excel_data = exporter.prepare_excel_data()
    
    # Vérifie les colonnes
    assert 'Time Interval' in excel_data.index
    assert 'Unit' in excel_data.index
    assert 'Month/Day Hour:Minute' in excel_data.index
    
    # Vérifie les valeurs
    assert excel_data.loc['Time Interval', 'Value'] == '60'
    assert excel_data.loc['Unit', 'Value'] == 'kW'

def test_export_to_excel(sample_data, tmp_path):
    """Teste l'export vers Excel"""
    output_file = tmp_path / "2023.xlsx"
    exporter = ExcelExporter(sample_data)
    exporter.export_to_excel(str(output_file))
    
    # Vérifie que le fichier existe
    assert os.path.exists(output_file)
    
    # Vérifie le contenu du fichier
    df = pd.read_excel(output_file, engine='openpyxl')
    assert 'Time Interval' in df.iloc[0].values
    assert 'Unit' in df.iloc[1].values
    assert 'Month/Day Hour:Minute' in df.iloc[2].values

def test_validate_export_format(sample_data, tmp_path):
    """Teste la validation du format d'export"""
    output_file = tmp_path / "2023.xlsx"
    exporter = ExcelExporter(sample_data)
    exporter.export_to_excel(str(output_file))
    
    # Vérifie le format du fichier exporté
    validation_errors = exporter.validate_export_format(str(output_file))
    assert len(validation_errors) == 0
