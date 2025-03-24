"""
Tests pour le module de lecture des données ENEDIS
"""  # pylint: disable=redefined-outer-name

from pathlib import Path
import pytest
import pandas as pd
from solarcalculet.data_reader import DataReader


@pytest.fixture
def sample_data_path(tmp_path):
    """Crée un fichier CSV de test"""
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
    data = ";".join(headers) + "\n"
    data += (
        "19125759625988;2023-03-13 00:00:00;2025-03-13 00:00:00;PA;CONS;BRUT;W;"
        "2023-03-13 00:30:00;692;B;PT30M;0;0\n"
    )
    data += (
        "19125759625988;2023-03-13 00:00:00;2025-03-13 00:00:00;PA;CONS;BRUT;W;"
        "2023-03-13 01:00:00;1284;B;PT30M;0;0"
    )
    csv_file = tmp_path / "test_enedis.csv"
    csv_file.write_text(data)
    return csv_file


def test_data_reader_init():
    """Teste l'initialisation du DataReader"""
    reader = DataReader("dummy.csv")
    assert isinstance(reader, DataReader)
    assert reader.file_path == Path("dummy.csv")


def test_read_csv_file(sample_data_path):
    """Teste la lecture du fichier CSV"""
    reader = DataReader(sample_data_path)
    df = reader.read()

    assert isinstance(df, pd.DataFrame)
    assert "Horodate" in df.columns
    assert "Valeur" in df.columns
    assert len(df) == 2


def test_validate_required_columns(sample_data_path):
    """Teste la validation des colonnes requises"""
    reader = DataReader(sample_data_path)
    df = reader.read()
    missing_cols = reader.validate_columns(df)
    assert len(missing_cols) == 0


def test_validate_missing_columns(tmp_path):
    """Teste la détection des colonnes manquantes"""
    # Créer un CSV avec des colonnes manquantes
    data = "Col1;Col2\n1;2\n3;4"
    csv_file = tmp_path / "invalid.csv"
    csv_file.write_text(data)

    reader = DataReader(csv_file)
    df = reader.read()
    missing_cols = reader.validate_columns(df)
    assert "Horodate" in missing_cols
    assert "Valeur" in missing_cols


def test_convert_values_to_kw(sample_data_path):
    """Teste la conversion des valeurs de W en kW"""
    reader = DataReader(sample_data_path)
    df = reader.read()
    df = reader.convert_to_kw(df)

    # La première valeur était 692 W, donc devrait être 0.692 kW
    assert df.iloc[0]["Valeur"] == 0.692
