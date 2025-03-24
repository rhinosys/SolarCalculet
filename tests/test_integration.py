"""
Tests d'intégration du processus complet
"""

import pytest
import pandas as pd
from solarcalculet.data_reader import DataReader
from solarcalculet.data_cleaner import DataCleaner
from solarcalculet.excel_exporter import ExcelExporter


@pytest.fixture
def input_csv(tmp_path):
    """Crée un fichier CSV de test avec des données sur 2023-2024"""
    headers = [
        "Identifiant PRM",
        "Date de début",
        "Date de fin",
        "Grandeur physique",
        "Grandeur métier",
        "Etape métier",
        "Unité",
        "Horodate",
        "Valeur",
        "Nature",
        "Pas",
        "Indice de vraisemblance",
        "Etat complémentaire",
    ]
    data_rows = [
        "19125759625988;2023-01-01 00:00:00;2024-12-31 23:59:59;PA;CONS;BRUT;W;2023-01-01 00:00:00;500;B;PT30M;0;0",
        "19125759625988;2023-01-01 00:00:00;2024-12-31 23:59:59;PA;CONS;BRUT;W;2023-01-01 01:00:00;600;B;PT30M;0;0",
        "19125759625988;2023-01-01 00:00:00;2024-12-31 23:59:59;PA;CONS;BRUT;W;2023-01-01 03:00:00;700;B;PT30M;0;0",
        "19125759625988;2023-01-01 00:00:00;2024-12-31 23:59:59;PA;CONS;BRUT;W;2024-01-01 00:00:00;550;B;PT30M;0;0",
        "19125759625988;2023-01-01 00:00:00;2024-12-31 23:59:59;PA;CONS;BRUT;W;2024-01-01 01:00:00;650;B;PT30M;0;0",
        "19125759625988;2023-01-01 00:00:00;2024-12-31 23:59:59;PA;CONS;BRUT;W;2024-01-01 02:00:00;750;B;PT30M;0;0",
    ]
    data = ";".join(headers) + "\n" + "\n".join(data_rows)

    csv_file = tmp_path / "ENEDIS.input.csv"
    csv_file.write_text(data)
    return csv_file


def test_full_process(input_csv, tmp_path):
    """
    Teste le processus complet :
    1. Lecture du fichier CSV
    2. Nettoyage des données
    3. Export vers Excel
    """
    # 1. Lecture des données
    reader = DataReader(input_csv)
    df = reader.read()
    assert not df.empty
    assert "Horodate" in df.columns
    assert "Valeur" in df.columns

    # Conversion en kW
    df = reader.convert_to_kw(df)
    assert df.iloc[0]["Valeur"] == 0.5  # 500W = 0.5kW

    # 2. Nettoyage des données
    cleaner = DataCleaner(df)

    # Vérifie la détection des données manquantes pour 2023
    missing_2023 = cleaner.detect_missing_hours("2023")
    assert len(missing_2023) == 1  # Il manque 2h dans les données 2023

    # Remplit les données manquantes
    filled_df = cleaner.fill_missing_data("2023")
    assert len(filled_df[filled_df["Horodate"].dt.year == 2023]) == 4

    # 3. Export vers Excel
    output_2023 = tmp_path / "2023.xlsx"
    output_2024 = tmp_path / "2024.xlsx"

    # Export 2023
    data_2023 = filled_df[filled_df["Horodate"].dt.year == 2023]
    exporter_2023 = ExcelExporter(data_2023)
    exporter_2023.export_to_excel(str(output_2023))

    # Export 2024
    data_2024 = filled_df[filled_df["Horodate"].dt.year == 2024]
    exporter_2024 = ExcelExporter(data_2024)
    exporter_2024.export_to_excel(str(output_2024))

    # Vérifie que les fichiers existent
    assert output_2023.exists()
    assert output_2024.exists()

    # Valide le format des fichiers
    assert len(exporter_2023.validate_export_format(str(output_2023))) == 0
    assert len(exporter_2024.validate_export_format(str(output_2024))) == 0

    # Vérifie le contenu des fichiers Excel
    df_2023 = pd.read_excel(output_2023, engine="openpyxl")
    df_2024 = pd.read_excel(output_2024, engine="openpyxl")

    assert "Time Interval" in df_2023.iloc[0].values
    assert "kW" in df_2023.iloc[1].values
    assert "Time Interval" in df_2024.iloc[0].values
    assert "kW" in df_2024.iloc[1].values
