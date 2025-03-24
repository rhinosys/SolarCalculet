# SolarCalculet - Outil de Nettoyage des Données ENEDIS

SolarCalculet est un outil Python conçu pour nettoyer et traiter les données de consommation d'énergie provenant d'ENEDIS. Il permet de gérer les données manquantes, valider les formats, et générer des fichiers de sortie organisés par année.

## Table des Matières

1. [Installation](#installation)
2. [Utilisation](#utilisation)
3. [Structure du Projet](#structure-du-projet)
4. [Tests](#tests)
5. [Documentation Technique](#documentation-technique)

## Installation

1. Clonez le dépôt :
```bash
git clone https://github.com/votre-compte/SolarCalculet.git
cd SolarCalculet
```

2. Créez un environnement virtuel et installez les dépendances :
```bash
python -m venv venv
source venv/bin/activate  # Sur Unix/macOS
pip install -r requirements.txt
```

3. Installez et démarrez MongoDB :
```bash
# Sur macOS avec Homebrew
brew tap mongodb/brew
brew install mongodb-community
brew services start mongodb/brew/mongodb-community
```

## Utilisation

1. Placez votre fichier de données ENEDIS dans le répertoire `Data/` avec le nom suivant :
```
ENEDIS_R63_P_CdC_M07VD2PL_00001_[DATE].csv
```

2. Exécutez le script principal :
```bash
python src/main.py
```

3. Les fichiers de sortie seront générés dans le répertoire `Data/` :
- `2023.csv` : Données pour l'année 2023
- `2024.csv` : Données pour l'année 2024

## Structure du Projet

```
SolarCalculet/
├── src/
│   ├── data_cleaner.py   # Classe principale de nettoyage
│   └── main.py           # Script principal
├── tests/
│   ├── test_data_cleaner.py  # Tests unitaires
│   └── test_integration.py   # Tests d'intégration
├── Data/                 # Données d'entrée/sortie
└── docs/                # Documentation
```

## Tests

Le projet utilise pytest pour les tests unitaires et d'intégration.

### Tests Unitaires

Les tests unitaires (`test_data_cleaner.py`) vérifient chaque composant individuellement :

1. **Configuration et Connexion**
   - Test d'initialisation de DataCleaner
   - Test de connexion à MongoDB

2. **Lecture et Validation**
   - Test de lecture de fichier CSV
   - Test de validation du format des données
   - Test de détection des données manquantes

3. **Traitement des Données**
   - Test de recherche des données de remplacement
   - Test de complétion des données manquantes
   - Test de validation des données complétées

4. **Stockage et Export**
   - Test de stockage dans MongoDB
   - Test d'organisation par année
   - Test de génération des fichiers

### Tests d'Intégration

Les tests d'intégration (`test_integration.py`) vérifient le processus complet :

1. **Test de Bout en Bout**
   - Lecture des données
   - Validation et nettoyage
   - Stockage dans MongoDB
   - Génération des fichiers

2. **Test de Cohérence**
   - Vérification des données d'origine
   - Validation des données complétées
   - Cohérence entre entrée et sortie

Pour exécuter les tests :
```bash
pytest tests/ -v
```

## Documentation Technique

### DataCleaner

Classe principale gérant le nettoyage des données :

```python
class DataCleaner:
    def __init__(self):
        """Initialise le nettoyeur de données."""
        
    def connect_to_mongodb(self) -> bool:
        """Établit la connexion à MongoDB."""
        
    def read_csv_file(self, file_path: str) -> pd.DataFrame:
        """Lit le fichier CSV des données ENEDIS."""
        
    def validate_data_format(self, df: pd.DataFrame) -> dict:
        """Valide le format des données."""
        
    def complete_missing_data(self, df: pd.DataFrame) -> pd.DataFrame:
        """Complète les données manquantes."""
        
    def store_data_in_mongodb(self, df: pd.DataFrame) -> bool:
        """Stocke les données dans MongoDB."""
        
    def generate_output_files(self, df: pd.DataFrame, output_dir: str) -> bool:
        """Génère les fichiers de sortie par année."""
```

### Format des Données

#### Entrée
```csv
Horodate;Consommation (Wh)
2023-01-01 00:00:00;120
2023-01-01 01:00:00;115
```

#### Sortie
Les fichiers de sortie conservent le même format mais sont organisés par année et ne contiennent que des données valides et complètes.

### Gestion des Erreurs

1. **Données Manquantes**
   - Recherche dans les années suivantes
   - Remplacement par les valeurs correspondantes

2. **Données Invalides**
   - Détection des formats incorrects
   - Exclusion des données non numériques

3. **Validation**
   - Vérification des types de données
   - Validation des plages horaires
   - Contrôle de cohérence

## Contribution

1. Fork le projet
2. Créez votre branche (`git checkout -b feature/AmazingFeature`)
3. Committez vos changements (`git commit -m 'Add some AmazingFeature'`)
4. Push vers la branche (`git push origin feature/AmazingFeature`)
5. Ouvrez une Pull Request

## Licence

Ce projet est sous licence MIT. Voir le fichier `LICENSE` pour plus de détails.
