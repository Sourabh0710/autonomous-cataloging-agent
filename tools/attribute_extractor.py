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


def extract_json(text):

    match = re.search(r"\{.*\}", text, re.DOTALL)

    if match:
        return match.group()

    return "{}"


def extract_attributes(text):

    prompt = ChatPromptTemplate.from_template("""
Extract product attributes from the text.

Text:
{text}

Return ONLY valid JSON.

Format:
{{
    "color": "",
    "material": "",
    "category": ""
}}

STRICT RULES:
- No markdown
- No explanations
- JSON only
""")

    chain = prompt | llm

    response = chain.invoke({
        "text": text
    })

    raw_response = response.content

    cleaned_response = extract_json(raw_response)

    return json.loads(cleaned_response)