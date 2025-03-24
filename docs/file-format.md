# Format des Fichiers

## Fichier d'Entrée (CSV)

Le fichier d'entrée doit être au format CSV avec les caractéristiques suivantes :

### Format
- Séparateur : point-virgule (`;`)
- Encodage : UTF-8
- Extension : `.csv`

### Colonnes Requises
- `Horodate` : Date et heure de la mesure (format : `YYYY-MM-DD HH:mm:ss`)
- `Valeur` : Valeur de consommation en watts (W)

### Exemple
```csv
Identifiant PRM;Date de début;Date de fin;Grandeur physique;Grandeur métier;Etape métier;Unité;Horodate;Valeur;Nature;Pas;Indice de vraisemblance;Etat complémentaire
19125759625988;2023-03-13 00:00:00;2025-03-13 00:00:00;PA;CONS;BRUT;W;2023-03-13 00:30:00;692;B;PT30M;0;0
19125759625988;2023-03-13 00:00:00;2025-03-13 00:00:00;PA;CONS;BRUT;W;2023-03-13 01:00:00;1284;B;PT30M;0;0
```

## Fichiers de Sortie (XLSX)

Les fichiers de sortie sont au format Excel (`.xlsx`) avec une structure spécifique.

### Caractéristiques
- Un fichier par année (`2023.xlsx`, `2024.xlsx`)
- Valeurs converties en kilowatts (kW)
- Intervalle horaire : 60 minutes
- Format de date : "Month/Day Hour:Minute"

### Structure du Fichier

1. **En-tête (Lignes 1-4)**
   ```
   Note: [Instructions détaillées]
   Time Interval: 60
   Unit: kW
   Month/Day Hour:Minute | Load Power
   ```

2. **Données (à partir de la ligne 5)**
   ```
   1/1 0:00 | 0.692
   1/1 1:00 | 1.284
   1/1 2:00 | 0.842
   ...
   ```

### Notes Importantes
- Les valeurs sont converties de W en kW (divisées par 1000)
- Les données manquantes sont complétées automatiquement
- Une colonne "Source" indique l'origine des données complétées

### Validation du Format
Le module `ExcelExporter` effectue plusieurs validations :
1. Présence des éléments requis
2. Intervalle de temps correct (60 minutes)
3. Unité correcte (kW)
4. Format des dates conforme
