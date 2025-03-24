"""
Configuration des tests pytest.
"""
import pytest
import os
import sys

# Ajoute le répertoire src au PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture(scope="session")
def test_data_dir():
    """Retourne le chemin vers le répertoire de données de test."""
    return os.path.join(os.path.dirname(__file__), 'test_data')
