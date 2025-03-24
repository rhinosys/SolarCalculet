# SolarCalculet Documentation

## Introduction

SolarCalculet est un outil Python conçu pour nettoyer et traiter les données de consommation électrique ENEDIS. Il permet de :
- Lire les données depuis un fichier CSV ENEDIS
- Détecter et compléter les données manquantes
- Générer des fichiers Excel formatés pour 2023 et 2024

## Installation

1. Cloner le dépôt :
```bash
git clone https://github.com/votre-compte/SolarCalculet.git
cd SolarCalculet
```

2. Créer un environnement virtuel :
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate  # Windows
```

3. Installer les dépendances :
```bash
pip install -r requirements.txt
```

## Utilisation

### Format du fichier d'entrée

Le fichier CSV ENEDIS doit contenir au minimum les colonnes suivantes :
- `Horodate` : Date et heure de la mesure
- `Valeur` : Valeur de consommation en W

Exemple :
```csv
Identifiant PRM;Horodate;Valeur;...
19125759625988;2023-01-01 00:00:00;500;...
```

### Exécution

```bash
python -m solarcalculet.main <input_csv> <output_dir>
```

Exemple :
```bash
python -m solarcalculet.main Data/ENEDIS.input.csv output/
```

### Format des fichiers de sortie

Les fichiers Excel générés (`2023.xlsx` et `2024.xlsx`) suivent un format spécifique :

1. **En-tête**
   - Note explicative
   - Time Interval : 60 (minutes)
   - Unit : kW
   - Column A : "Month/Day Hour:Minute"

2. **Données**
   - Format de date : "M/D H:mm" (ex: "1/1 0:00")
   - Valeurs en kW (converties depuis les watts)
   - Données manquantes complétées automatiquement

## Architecture du Code

### Structure du projet
```
SolarCalculet/
├── src/
│   └── solarcalculet/
│       ├── __init__.py
│       ├── data_reader.py
│       ├── data_cleaner.py
│       ├── excel_exporter.py
│       └── main.py
├── tests/
│   ├── test_config.py
│   ├── test_data_reader.py
│   ├── test_data_cleaner.py
│   ├── test_excel_exporter.py
│   └── test_integration.py
└── requirements.txt
```

### Modules

1. **DataReader** (`data_reader.py`)
   - Lecture du fichier CSV
   - Validation des colonnes
   - Conversion des valeurs en kW

2. **DataCleaner** (`data_cleaner.py`)
   - Détection des heures manquantes
   - Recherche des données de substitution
   - Remplissage automatique avec traçabilité

3. **ExcelExporter** (`excel_exporter.py`)
   - Formatage des dates
   - Génération des fichiers Excel
   - Validation du format

## Tests

Le projet suit une approche TDD (Test Driven Development). Les tests sont organisés par module :

```bash
# Exécuter tous les tests
pytest

# Exécuter un module spécifique
pytest tests/test_data_reader.py -v

# Exécuter les tests d'intégration
pytest tests/test_integration.py -v
```

### Types de tests

1. **Tests unitaires**
   - `test_config.py` : Configuration et dépendances
   - `test_data_reader.py` : Lecture des données
   - `test_data_cleaner.py` : Nettoyage des données
   - `test_excel_exporter.py` : Export Excel

2. **Tests d'intégration**
   - `test_integration.py` : Processus complet
   - Validation du format final

## Journal de Développement

Pour suivre l'évolution du projet, consultez le [DEVBOOK.md](../DEVBOOK.md).
