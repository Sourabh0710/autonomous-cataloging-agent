import pandas as pd

def export_csv(products,output_path):

    df = pd.DataFrame(products)

    df.to_csv(output_path,index=False)

    print(f"\nCSV exported successfully to: {output_path}")

    