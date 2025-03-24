"""
Tests de configuration initiale
"""
import pytest
from solarcalculet import __version__

def test_version():
    """Vérifie que la version est définie"""
    assert __version__ == '0.1.0'

def test_dependencies():
    """Vérifie que les dépendances principales sont disponibles"""
    import pandas as pd
    import openpyxl
    import pymongo
    
    assert pd.__version__ >= '2.0.0'
