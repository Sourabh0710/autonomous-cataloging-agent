from typing import TypedDict, List, Dict, Any

import pandas as pd

from langgraph.graph import StateGraph, END

from tools.inspect_excel import inspect_excel
from tools.schema_mapper import map_schema
from tools.cleaner import clean_value
from tools.exporter import export_csv
from tools.attribute_extractor import extract_attributes

from models.product_schema import Product


# AGENT STATE


class CatalogState(TypedDict):

    file_path: str

    inspection: Dict[str, Any]

    columns: List[str]

    mapping: Dict[str, str]

    dataframe: Any

    products: List[Dict]


# NODE 1 — INSPECT EXCEL


def inspect_node(state: CatalogState):

    print("\n[AGENT] Inspecting workbook...")

    inspection = inspect_excel(state["file_path"])

    sheet_name = list(inspection.keys())[0]

    columns = inspection[sheet_name]["columns"]

    df = pd.read_excel(
        state["file_path"],
        sheet_name=sheet_name
    )

    return {
        **state,
        "inspection": inspection,
        "columns": columns,
        "dataframe": df
    }


# NODE 2 — GENERATE SCHEMA MAPPING


def mapping_node(state: CatalogState):

    print("\n[AGENT] Generating schema mapping...")

    mapping = map_schema(state["columns"])

    print("\n[AGENT] Generated Schema Mapping:")
    print(mapping)

    if "selling_price" in mapping:
        print("\n[AGENT] Using selling_price as transactional price.")
    elif "mrp" in mapping:
        print("\n[AGENT] selling_price unavailable. Falling back to mrp.")

    return {
        **state,
        "mapping": mapping
    }


# NODE 3 — TRANSFORM PRODUCTS


def transform_node(state: CatalogState):

    print("\n[AGENT] Transforming products...")

    products = []

    df = state["dataframe"]

    mapping = state["mapping"]

    for _, row in df.iterrows():

        product_data = {}

        for vendor_col, standard_field in mapping.items():

            value = row.get(vendor_col, "")

            value = clean_value(value)

            product_data[standard_field] = value

        # ATTRIBUTE EXTRACTION

        combined_text = (
            f"{product_data.get('name', '')} "
            f"{product_data.get('description', '')}"
        )

        extracted = extract_attributes(combined_text)

        if not product_data.get("color"):
            product_data["color"] = extracted.get("color", "")

        if not product_data.get("material"):
            product_data["material"] = extracted.get("material", "")

        if not product_data.get("category"):
            product_data["category"] = extracted.get("category", "")

        # CLEAN PRICE

        try:
            product_data["price"] = float(
                product_data.get("price", 0)
            )
        except:
            product_data["price"] = 0.0

        standardized_product = Product(
            sku=product_data.get("sku", ""),
            name=product_data.get("name", ""),
            description=product_data.get("description", ""),
            brand=product_data.get("brand", ""),
            category=product_data.get("category", ""),
            color=product_data.get("color", ""),
            size=product_data.get("size", ""),
            material=product_data.get("material", ""),
            price=product_data.get("price", 0.0),
            image_url_1=product_data.get("image_url_1", ""),
            image_url_2=product_data.get("image_url_2", ""),
            image_url_3=product_data.get("image_url_3", "")
        )

        products.append(
            standardized_product.model_dump()
        )

    return {
        **state,
        "products": products
    }


# NODE 4 — EXPORT CSV


def export_node(state: CatalogState):

    print("\n[AGENT] Exporting standardized catalog...")

    export_csv(
        state["products"],
        "outputs/standardized_catalog.csv"
    )

    return state


# BUILD GRAPH


workflow = StateGraph(CatalogState)

workflow.add_node(
    "inspect",
    inspect_node
)

workflow.add_node(
    "mapping",
    mapping_node
)

workflow.add_node(
    "transform",
    transform_node
)

workflow.add_node(
    "export",
    export_node
)


workflow.set_entry_point("inspect")

workflow.add_edge("inspect", "mapping")

workflow.add_edge("mapping", "transform")

workflow.add_edge("transform", "export")

workflow.add_edge("export", END)


catalog_agent = workflow.compile()