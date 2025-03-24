# Tests et Qualité du Code

## Approche TDD

Le projet suit une approche Test-Driven Development (TDD) :

1. **Écriture des tests** : Définition du comportement attendu
2. **Implémentation** : Développement pour faire passer les tests
3. **Refactoring** : Amélioration du code sans casser les tests

## Structure des Tests

### Tests Unitaires

1. **Configuration (`test_config.py`)**
   ```python
   def test_version():
       """Vérifie que la version est correctement définie"""
       from solarcalculet import __version__
       assert __version__ == "1.0.0"
   ```

2. **Lecture des Données (`test_data_reader.py`)**
   ```python
   def test_read_csv():
       """Vérifie la lecture du fichier CSV"""
       reader = DataReader("test.csv")
       df = reader.read()
       assert "Horodate" in df.columns
       assert "Valeur" in df.columns
   ```

3. **Nettoyage des Données (`test_data_cleaner.py`)**
   ```python
   def test_detect_missing_hours():
       """Vérifie la détection des heures manquantes"""
       cleaner = DataCleaner(df)
       missing = cleaner.detect_missing_hours("2023")
       assert len(missing) == 1
   ```

4. **Export Excel (`test_excel_exporter.py`)**
   ```python
   def test_format_excel():
       """Vérifie le format du fichier Excel"""
       exporter = ExcelExporter(df)
       assert exporter.validate_format()
   ```

### Tests d'Intégration

Le fichier `test_integration.py` teste le processus complet :

```python
def test_full_process():
    """Test le processus complet de traitement"""
    # 1. Lecture des données
    reader = DataReader("test.csv")
    df = reader.read()
    
    # 2. Nettoyage
    cleaner = DataCleaner(df)
    cleaned_data = cleaner.process()
    
    # 3. Export
    exporter = ExcelExporter(cleaned_data)
    exporter.export("output/test.xlsx")
    
    # 4. Validation
    assert Path("output/test.xlsx").exists()
```

## Exécution des Tests

### Commandes de Base
```bash
# Tous les tests
pytest

# Tests spécifiques
pytest tests/test_data_reader.py

# Mode verbeux
pytest -v

# Avec couverture
pytest --cov=src/solarcalculet
```

### Configuration pytest

Le fichier `pytest.ini` définit les paramètres de test :
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

## Qualité du Code

### Outils Utilisés
1. **pytest** : Tests unitaires et d'intégration
2. **coverage** : Couverture de code
3. **pylint** : Style de code
4. **black** : Formatage automatique

### Bonnes Pratiques
1. Tests isolés et indépendants
2. Utilisation de fixtures pytest
3. Tests des cas limites
4. Documentation des tests
5. Assertions explicites

## Résultats des Tests

Les tests sont exécutés automatiquement à chaque commit :

```bash
============================= test session starts ==============================
platform darwin -- Python 3.13.2, pytest-8.3.5
plugins: hypothesis-6.75.3, cov-4.1.0
collected 32 items

tests/test_config.py ........                                          [ 25%]
tests/test_data_reader.py ........                                     [ 50%]
tests/test_data_cleaner.py ........                                    [ 75%]
tests/test_excel_exporter.py ........                                  [100%]

============================== 32 passed in 2.34s ============================
```
