"""
Script principal pour le nettoyage des données ENEDIS.
"""
import os
from data_cleaner import DataCleaner

def main():
    """Fonction principale."""
    try:
        # Initialisation
        cleaner = DataCleaner()
        if not cleaner.connect_to_mongodb():
            print("Erreur de connexion à MongoDB")
            return False
            
        # Lecture du fichier d'entrée
        input_file = "./Data/ENEDIS_R63_P_CdC_M07VD2PL_00001_20250313093019.csv"
        if not os.path.exists(input_file):
            print(f"Fichier d'entrée non trouvé : {input_file}")
            return False
            
        print("Lecture des données...")
        df = cleaner.read_csv_file(input_file)
        
        # Validation initiale
        print("Validation des données...")
        validation = cleaner.validate_data_format(df)
        if validation['invalid_rows'] or validation['missing_values']:
            print(f"Trouvé {len(validation['invalid_rows'])} lignes invalides et "
                  f"{len(validation['missing_values'])} valeurs manquantes")
        
        # Complétion des données
        print("Complétion des données manquantes...")
        df_completed = cleaner.complete_missing_data(df)
        
        # Validation finale
        validation_completed = cleaner.validate_completed_data(df_completed)
        if not validation_completed['is_valid']:
            print("Erreur dans la validation finale :")
            for error in validation_completed['errors']:
                print(f"- {error}")
            return False
        
        # Stockage dans MongoDB
        print("Stockage dans MongoDB...")
        if not cleaner.store_data_in_mongodb(df_completed):
            print("Erreur lors du stockage dans MongoDB")
            return False
        
        # Génération des fichiers
        print("Génération des fichiers de sortie...")
        if not cleaner.generate_output_files(df_completed, "./Data"):
            print("Erreur lors de la génération des fichiers")
            return False
        
        print("Traitement terminé avec succès !")
        print("Fichiers générés : ./Data/2023.csv et ./Data/2024.csv")
        return True
        
    except Exception as e:
        print(f"Erreur lors du traitement : {e}")
        return False

if __name__ == "__main__":
    main()
