# Journal de développement - Nettoyage des données ENEDIS

## Objectif
Créer un outil de nettoyage pour le fichier de données ENEDIS avec complétion des données manquantes à partir des années 2023/2024/2025.

## Étapes du projet

### 1. Configuration initiale
- [x] Mise en place de l'environnement de développement Python
- [x] Configuration des outils de test (pytest)
- [x] Création de la structure du projet
- [x] Configuration de MongoDB

### 2. Lecture et validation des données (TDD)
- [x] Tests et implémentation de la lecture du fichier CSV
- [x] Tests et implémentation de la validation du format des données
- [x] Tests et implémentation de la détection des données manquantes

### 3. Traitement des données manquantes (TDD)
- [x] Tests et implémentation de la recherche des données de substitution
- [x] Tests et implémentation de la logique de remplacement (2023/2024/2025)
- [x] Tests et implémentation de la validation des données complétées

### 4. Stockage et organisation des données (TDD)
- [x] Tests et implémentation de l'interaction avec MongoDB
- [x] Tests et implémentation de la structuration des données par année
- [x] Tests et implémentation de la génération des fichiers de sortie

### 5. Export et vérification finale (TDD)
- [x] Tests et implémentation de l'export vers 2023.csv
- [x] Tests et implémentation de l'export vers 2024.csv
- [x] Tests d'intégration de bout en bout

## Technologies utilisées
- Python
- pytest pour les tests
- pandas pour la manipulation des données
- MongoDB pour le stockage intermédiaire

## Journal des modifications
*Les modifications seront ajoutées ici au fur et à mesure de l'avancement du projet*

Date | Description
-----|-------------
2025-03-24 | Configuration initiale : Création de la structure du projet, mise en place de l'environnement virtuel, configuration de pytest et MongoDB
2025-03-24 | Lecture et validation : Implémentation des fonctions de lecture CSV, validation des données et détection des données manquantes
2025-03-24 | Traitement des données : Implémentation de la recherche et du remplacement des données manquantes avec validation
2025-03-24 | Stockage et organisation : Installation de MongoDB, implémentation du stockage et de la génération des fichiers par année
2025-03-24 | Export et vérification : Implémentation des tests d'intégration et vérification du processus complet
