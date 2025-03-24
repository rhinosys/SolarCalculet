"""
Module d'export des données au format Excel
"""

import pandas as pd


class ExcelExporter:
    """Classe pour exporter les données au format Excel spécifié"""

    EXCEL_TEMPLATE = """
    Note:
    1. Do not delete this note or change the format, date & time column, or time interval in the template.
       Enter the load power for each time segment in each date. Do not leave any cell empty.
    2. The template contains all data from 0:00 on January 1 to the end of the year (365 days).
    3. Enter the unit of the load power (kW or W) in cell B3.
    4. Column A refers to "Month/Day Hour:Minute".
    5. Enter the load power at 0:00 on January 1 in cell B5, at 1:00 in cell B6, and so on.
    6. Each value must be greater than or equal to 0 (max 6 decimals for kW, 2 for W).
    """

    def __init__(self, data: pd.DataFrame):
        """
        Initialise l'exporteur Excel

        Args:
            data: DataFrame contenant les données à exporter
        """
        self.data = data.copy()

    def format_date_hour(self) -> pd.DataFrame:
        """
        Formate les dates et heures selon le template

        Returns:
            DataFrame avec les dates formatées
        """
        df = self.data.copy()
        df["Month/Day Hour:Minute"] = df["Horodate"].apply(
            lambda x: f"{x.month}/{x.day} {x.hour}:00"
        )
        return df

    def prepare_excel_data(self) -> pd.DataFrame:
        """
        Prépare les données pour l'export Excel

        Returns:
            DataFrame formaté selon le template
        """
        # Formate les données
        formatted_df = self.format_date_hour()

        # Crée le DataFrame pour Excel
        excel_data = pd.DataFrame(columns=["Value"])

        # Ajoute l'en-tête
        excel_data.loc["Note", "Value"] = self.EXCEL_TEMPLATE
        excel_data.loc["Time Interval", "Value"] = "60"
        excel_data.loc["Unit", "Value"] = "kW"
        excel_data.loc["Month/Day Hour:Minute", "Value"] = "Load Power"

        # Ajoute les données
        for _, row in formatted_df.iterrows():
            excel_data.loc[row["Month/Day Hour:Minute"], "Value"] = row["Valeur"]

        return excel_data

    def export_to_excel(self, output_file: str):
        """
        Exporte les données vers un fichier Excel

        Args:
            output_file: Chemin du fichier de sortie
        """
        excel_data = self.prepare_excel_data()

        # Configure le writer Excel
        writer = pd.ExcelWriter(output_file, engine="openpyxl")

        # Écrit les données
        excel_data.to_excel(writer, sheet_name="Sheet1", header=False)

        # Ajuste la largeur des colonnes
        worksheet = writer.sheets["Sheet1"]
        worksheet.column_dimensions["A"].width = 25
        worksheet.column_dimensions["B"].width = 15

        # Sauvegarde le fichier
        writer.close()

    def validate_export_format(self, excel_file: str) -> list:
        """
        Valide le format du fichier exporté

        Args:
            excel_file: Chemin du fichier à valider

        Returns:
            Liste des erreurs de validation
        """
        errors = []
        try:
            df = pd.read_excel(excel_file, engine="openpyxl")

            # Vérifie les éléments requis
            required_elements = ["Time Interval", "Unit", "Month/Day Hour:Minute"]
            for element in required_elements:
                if not any(df.iloc[:, 0].astype(str).str.contains(element)):
                    errors.append(f"Missing required element: {element}")

            # Vérifie l'intervalle de temps
            if "60" not in df.iloc[:, 1].astype(str).values:
                errors.append("Time Interval should be 60")

            # Vérifie l'unité
            if "kW" not in df.iloc[:, 1].astype(str).values:
                errors.append("Unit should be kW")

        except Exception as e:
            errors.append(f"Error validating file: {str(e)}")

        return errors
