from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
import json
import re

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    temperature=0
)

STANDARD_FIELDS = [
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


def extract_json(text):

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        return match.group()

    return "{}"


def map_schema(columns):

    # PRIORITIZE SELLING PRICE

    if "selling_price" in columns:
        preferred_price = "selling_price"
    elif "mrp" in columns:
        preferred_price = "mrp"
    else:
        preferred_price = None

    prompt = ChatPromptTemplate.from_template("""
You are an intelligent schema mapping agent.

Your task is to map ONLY the EXACT vendor columns
to the standardized catalog schema.

Vendor Columns:
{columns}

Target Standard Fields:
{standard_fields}

Preferred Price Column:
{preferred_price}

STRICT RULES:
- Use ONLY exact vendor column names from the provided list
- Do NOT invent new column names
- Return ONLY valid JSON
- No explanations
- No markdown
- Keys = vendor columns
- Values = standardized schema fields

IMPORTANT:
- selling_price should ALWAYS map to price if available
- use mrp ONLY if selling_price is unavailable
- main_image_url → image_url_1
- image_2 → image_url_2
- image_3 → image_url_3

Correct Example:
{{
    "selling_price": "price",
    "main_image_url": "image_url_1",
    "image_2": "image_url_2"
}}
""")

    chain = prompt | llm

    response = chain.invoke({
        "columns": columns,
        "standard_fields": STANDARD_FIELDS,
        "preferred_price": preferred_price
    })

    raw_response = response.content

    print("\nRAW LLM RESPONSE:")
    print(raw_response)

    cleaned_response = extract_json(raw_response)

    return json.loads(cleaned_response)