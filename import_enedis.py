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

def process_enedis_data(csv_path, template_path, output_path):
    # Lire le fichier CSV ENEDIS
    df_csv = pd.read_csv(csv_path, sep=";", encoding="utf-8")
    df_csv["Horodate"] = pd.to_datetime(df_csv["Horodate"])
    df_csv["Time Formatted"] = df_csv["Horodate"].dt.strftime("%-m/%-d %-H:%M")

    # Agréger les valeurs de consommation par heure
    df_hourly = df_csv.groupby(df_csv["Horodate"].dt.floor("h"))["Valeur"].sum().reset_index()
    df_hourly["Time Formatted"] = df_hourly["Horodate"].dt.strftime("%-m/%-d %-H:%M")
    
    # Charger le template Excel
    df_excel = pd.ExcelFile(template_path)
    df_template = df_excel.parse("sheet1")
    
    # Trouver la colonne où insérer les valeurs
    column_index = 1  # Première colonne après l'heure
    
    # Mise à jour du template avec les valeurs agrégées
    for _, row in df_hourly.iterrows():
        time_str = row["Time Formatted"]
        consumption = row["Valeur"]

        matching_row = df_template[df_template.iloc[:, 0] == time_str]
        if not matching_row.empty:

            index = matching_row.index[0]
            df_template.iloc[index, column_index] = consumption
    
    # Sauvegarde du fichier Excel rempli
    df_template.to_excel(output_path, index=False)
    print(f"Fichier traité et sauvegardé sous : {output_path}")


# Utilisation du script
data_directory = './data/2024'
print("Début du traitement des fichiers de consommation...")
data_transformed = process_consumption(data_directory)

if data_transformed is not None:
    output_file = './consommation_totale.csv'
    print(f"Enregistrement du fichier transformé dans: {output_file}")
    data_transformed.to_csv(output_file, index=False)
    print("Fichier transformé disponible.")


# Exemple d'utilisation
data_csv = "./Data/ENEDIS_R63_P_CdC_M07VD2PL_00001_20250313093019.csv"
template_excel = "./template_1.xlsx"
output_filled = "./filled_template.xlsx"

process_enedis_data(data_csv, template_excel, output_filled)
