import pandas as pd


def inspect_excel(file_path):

    excel = pd.ExcelFile(file_path)

    inspection = {}

    for sheet in excel.sheet_names:

        df = pd.read_excel(file_path, sheet_name=sheet)

        inspection[sheet] = {
            "columns": list(df.columns),
            "row_count": len(df),
            "sample_rows": df.head(3).to_dict(orient="records"),
            "missing_values": df.isnull().sum().to_dict()
        }

    return inspection