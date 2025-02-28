import pandas as pd
import os

def process_consumption(directory):
    all_data = []
    
    # Parcourir tous les fichiers Excel dans le dossier spécifié
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".xlsx"):
                file_path = os.path.join(root, file)
                print(f"Traitement du fichier : {file_path}")
                
                df = pd.ExcelFile(file_path)
                
                if 'Consommation Horaire' in df.sheet_names:
                    data = df.parse('Consommation Horaire')
                    start_row = 15  # Ajuster si nécessaire
                    data_cleaned = data.iloc[start_row:, [2, 4]]
                    data_cleaned.columns = ['Start Time', 'Consumption (kW)']
                    data_cleaned = data_cleaned.dropna().reset_index(drop=True)
                    
                    data_cleaned['Start Time'] = pd.to_datetime(data_cleaned['Start Time'], format='%d/%m/%Y %H:%M:%S', errors='coerce')
                    data_cleaned['Consumption (W)'] = data_cleaned['Consumption (kW)'].str.replace(',', '.').astype(float) * 1000
                    
                    all_data.append(data_cleaned[['Start Time', 'Consumption (W)']])
    
    if all_data:
        # Concaténer toutes les données
        combined_data = pd.concat(all_data).drop_duplicates().sort_values(by='Start Time')
        
        # Regrouper par heure et sommer les valeurs
        combined_data = combined_data.groupby(combined_data['Start Time'].dt.floor('h'))['Consumption (W)'].sum().reset_index()
        
        return combined_data
    else:
        print("Aucun fichier valide trouvé.")
        return None

# Utilisation du script
data_directory = '/Users/nrineau/Projects/SolarCalculet/data/2024'
print("Début du traitement des fichiers de consommation...")
data_transformed = process_consumption(data_directory)

if data_transformed is not None:
    output_file = '/Users/nrineau/Projects/SolarCalculet/consommation_totale.csv'
    print(f"Enregistrement du fichier transformé dans: {output_file}")
    data_transformed.to_csv(output_file, index=False)
    print("Fichier transformé disponible.")
