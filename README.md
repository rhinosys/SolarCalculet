# README - Importation et Traitement des Données de Consommation Électrique

## 📌 Description
Le script `import_enedis.py` permet d'importer, traiter et agréger des données de consommation électrique issues de fichiers Excel fournis par Enedis. Comme chaque fichier ne contient que 7 jours de données, ce script fusionne l’ensemble des fichiers disponibles et génère un fichier unique avec une consommation horaire agrégée.

## 🚀 Fonctionnalités
- Lecture de fichiers Excel contenant des données de consommation électrique.
- Extraction des valeurs de consommation par pas de 30 minutes.
- Conversion des valeurs de consommation de kW en Wh.
- Agrégation des données pour obtenir une consommation totale par heure.
- Génération d'un fichier CSV contenant les données consolidées.

## 📂 Structure des Données
Les fichiers Excel sont stockés dans le répertoire suivant :
```
/Users/nrineau/Projects/SolarCalculet/data/2024/
```
Chaque fichier représente une semaine et suit le format :
```
janvier.01.2024.xlsx
février.02.2024.xlsx
```

## 🔧 Installation et Prérequis
### 1️⃣ Installer Python 3.12 (si ce n'est pas déjà fait)
Si Python 3.12 n’est pas installé, installe-le avec :
```
brew install python@3.12  # macOS avec Homebrew
sudo apt install python3.12  # Linux (Ubuntu/Debian)
```
Vérifie l'installation avec :
```
python3.12 --version
```

### 2️⃣ Créer un environnement virtuel
Dans le dossier du projet, exécute :
```
python3.12 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate  # Windows
```

### 3️⃣ Installer les dépendances
Installe les bibliothèques nécessaires :
```
pip install pandas openpyxl
```

## ▶️ Utilisation
### 1️⃣ Exécuter le script
Lance le script avec la commande :
```
python import_enedis.py
```

### 2️⃣ Fichier de sortie
Le fichier consolidé sera généré à l’emplacement :
```
/Users/nrineau/Projects/SolarCalculet/consommation_totale.csv
```
Ce fichier contient les données sous le format suivant :
```
Start Time, Consumption (W)
2024-01-01 00:00:00, 4356
2024-01-01 01:00:00, 3982
...
```

## 🔍 Débogage et Logs
Le script affiche des messages pour suivre l'avancement :
- `Traitement du fichier : <nom_du_fichier>` → Indique quel fichier est en cours de traitement.
- `Aucun fichier valide trouvé.` → Aucun fichier Excel correct n'a été trouvé dans le dossier.
- `Enregistrement du fichier transformé dans: consommation_totale.csv` → Confirme la création du fichier final.

## 📌 Améliorations Possibles
- Ajouter un argument CLI pour spécifier le dossier source.
- Ajouter une gestion des erreurs plus robuste en cas de fichiers corrompus.
- Permettre une sortie au format JSON ou autre pour plus de flexibilité.

---

📧 **Contact** : Si vous avez des questions ou suggestions, n’hésitez pas à ouvrir une issue ou à contacter l’auteur. 🚀
