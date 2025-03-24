"""
Tests pour le module de nettoyage des données
"""

from datetime import datetime
import pytest
import pandas as pd
from solarcalculet.data_cleaner import DataCleaner


@pytest.fixture
def sample_data():
    """Crée un DataFrame de test avec des données manquantes"""
    data = {
        "Horodate": [
            "2023-01-01 00:00:00",
            "2023-01-01 01:00:00",
            # Trou de 2h manquant
            "2023-01-01 03:00:00",
            "2024-01-01 00:00:00",
            "2024-01-01 01:00:00",
            "2024-01-01 02:00:00",
            "2024-01-01 03:00:00",
        ],
        "Valeur": [0.5, 0.6, 0.8, 0.4, 0.5, 0.7, 0.9],
    }
    df = pd.DataFrame(data)
    df["Horodate"] = pd.to_datetime(df["Horodate"])
    return df


def test_detect_missing_hours(sample_data):
    """Teste la détection des heures manquantes"""
    cleaner = DataCleaner(sample_data)
    missing = cleaner.detect_missing_hours("2023")

    assert len(missing) == 1
    assert missing[0].hour == 2
    assert missing[0].date() == datetime(2023, 1, 1).date()


def test_find_replacement_data(sample_data):
    """Teste la recherche de données de remplacement"""
    cleaner = DataCleaner(sample_data)
    missing_dt = datetime(2023, 1, 1, 2, 0)
    replacement = cleaner.find_replacement_data(missing_dt)

    assert replacement is not None
    assert replacement == 0.7  # Valeur de 2024 pour la même heure


def test_fill_missing_data(sample_data):
    """Teste le remplissage des données manquantes"""
    cleaner = DataCleaner(sample_data)
    filled_df = cleaner.fill_missing_data("2023")

    # Vérifie que toutes les heures sont présentes
    hours_2023 = filled_df[filled_df["Horodate"].dt.year == 2023]
    assert len(hours_2023) == 4  # 4 heures au total

    # Vérifie que la valeur manquante a été remplacée
    missing_hour = filled_df[filled_df["Horodate"] == datetime(2023, 1, 1, 2, 0)]
    assert len(missing_hour) == 1
    assert missing_hour.iloc[0]["Valeur"] == 0.7
    assert missing_hour.iloc[0]["Source"] == "2024"  # Vérifie la source de la donnée


def test_get_data_by_year(sample_data):
    """Teste l'extraction des données par année"""
    cleaner = DataCleaner(sample_data)
    data_2023 = cleaner.get_data_by_year("2023")
    data_2024 = cleaner.get_data_by_year("2024")

    assert len(data_2023) == 3
    assert len(data_2024) == 4
    assert all(dt.year == 2023 for dt in data_2023["Horodate"])
    assert all(dt.year == 2024 for dt in data_2024["Horodate"])
