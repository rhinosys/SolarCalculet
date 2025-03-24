"""
Script principal pour le traitement des données ENEDIS
"""

import sys
from pathlib import Path
from solarcalculet.data_reader import DataReader
from solarcalculet.data_cleaner import DataCleaner
from solarcalculet.excel_exporter import ExcelExporter


def process_enedis_data(input_file: str, output_dir: str):
    """
    Traite les données ENEDIS et génère les fichiers Excel

    Args:
        input_file: Chemin du fichier CSV d'entrée
        output_dir: Répertoire de sortie pour les fichiers Excel
    """
    # Crée le répertoire de sortie si nécessaire
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 1. Lecture des données
    print(f"Lecture du fichier {input_file}...")
    reader = DataReader(input_file)
    df = reader.read()

    # Vérifie les colonnes requises
    missing_cols = reader.validate_columns(df)
    if missing_cols:
        raise ValueError(f"Colonnes manquantes : {', '.join(missing_cols)}")

    # Conversion en kW
    df = reader.convert_to_kw(df)
    print("Données converties en kW")

    # 2. Nettoyage des données
    print("Nettoyage des données...")
    cleaner = DataCleaner(df)

    # Traite chaque année
    for year in ["2023", "2024"]:
        print(f"\nTraitement de l'année {year}:")

        # Détecte les données manquantes
        missing = cleaner.detect_missing_hours(year)
        if missing:
            print(f"- {len(missing)} heures manquantes détectées")

            # Remplit les données manquantes
            df = cleaner.fill_missing_data(year)
            print("- Données manquantes complétées")
        else:
            print("- Aucune donnée manquante")

        # Extrait les données de l'année
        year_data = cleaner.get_data_by_year(year)

        # 3. Export vers Excel
        output_file = output_path / f"{year}.xlsx"
        print(f"- Génération du fichier {output_file}")

        exporter = ExcelExporter(year_data)
        exporter.export_to_excel(str(output_file))

        # Valide le format
        errors = exporter.validate_export_format(str(output_file))
        if errors:
            print(f"⚠️ Erreurs de validation pour {year}.xlsx:")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"✅ Fichier {year}.xlsx généré avec succès")

    print("\nTraitement terminé !")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python -m solarcalculet.main <input_csv> <output_dir>")
        sys.exit(1)

    process_enedis_data(sys.argv[1], sys.argv[2])
