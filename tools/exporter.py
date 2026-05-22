import pandas as pd


STANDARD_COLUMNS = [
    "sku",
    "name",
    "description",
    "brand",
    "category",
    "color",
    "size",
    "material",
    "price",
    "image_url_1",
    "image_url_2",
    "image_url_3"
]


def export_csv(products, output_path):

    # CREATE DATAFRAME WITH EXPLICIT COLUMNS

    df = pd.DataFrame(products)

    # ENSURE ALL REQUIRED COLUMNS EXIST

    for column in STANDARD_COLUMNS:

        if column not in df.columns:
            df[column] = ""

    # FORCE EXACT COLUMN ORDER

    df = df.loc[:, STANDARD_COLUMNS]

    # RESET COLUMN NAMES EXPLICITLY

    df.columns = STANDARD_COLUMNS

    # EXPORT CSV WITH HEADERS

    df.to_csv(
        output_path,
        index=False,
        columns=STANDARD_COLUMNS,
        header=STANDARD_COLUMNS
    )

    print(f"\nCSV exported successfully to: {output_path}")
