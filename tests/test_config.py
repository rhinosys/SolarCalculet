"""
Tests de configuration initiale
"""

import pandas as pd
from solarcalculet import __version__


def test_version():
    """Vérifie que la version est définie"""
    assert __version__ == "0.1.0"


def test_dependencies():
    """Vérifie que les dépendances principales sont disponibles"""
    assert pd.__version__ >= "2.0.0"
