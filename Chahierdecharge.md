# Cahier des Charges - Outil de Traitement des Données ENEDIS

## Objectif
Créer un outil de nettoyage pour le fichier `./Data/ENEDIS.input.csv`. Ce fichier est une extraction des données de consommation électrique provenant du distributeur énergétique de ma maison.

## Description des Données
- Le fichier contient les données de consommation horaire
- Période couverte : de 2023 à 2024
- Format : une ligne par heure de consommation

## Traitement Requis
1. Vérifier la complétude des données pour chaque jour de 2023 et 2024
2. En cas de données manquantes pour une heure :
   - Utiliser les données de la même heure de l'année 2024, 2023 ou 2025
   - Choisir la meilleure méthode de substitution

## Format d'Entrée
- Fichier : `ENEDIS.input.csv`
- Colonnes requises :
  - `Horodate` : date et heure de la mesure
  - `Valeur` : valeur de consommation
- Note : Le fichier peut contenir d'autres colonnes, mais seules `Horodate` et `Valeur` sont nécessaires

## Format de Sortie
1. Générer deux fichiers :
   - `2023.xlsx`
   - `2024.xlsx`
2. Format XLSX avec le modèle suivant :

'
"Note:
 1. Do not delete this note or change the format, date & time column, or time interval in the template. Enter the load power for each time segment in each date. Do not leave any cell empty.
 2. The template contains all data from 0:00 on January 1 to the end of the year (365 days).
 3. Enter the unit of the load power (kW or W) in cell B3.
 4. Column A refers to ""Month/Day Hour:Minute"".
 5. Enter the load power at 0:00 on January 1 in cell B5, the load power at 1:00 on January 1 in cell B6, and so on.
 6. Each value must be greater than or equal to 0. If you set the unit to kW, you can enter a maximum of six decimal places for each value. If you set the unit to W, you can enter a maximum of two decimal places for each value."	"
"	"
"	"
"	"
"	"
"	"
"	"
"	"
"
Time Interval	60							
Unit	kW							
Month/Day Hour:Minute	Load Power							
1/1 0:00								
1/1 1:00								
1/1 2:00								
1/1 3:00								
1/1 4:00								
1/1 5:00								
1/1 6:00								
1/1 7:00								
1/1 8:00								
1/1 9:00								
1/1 10:00								
'

Coder en python.
