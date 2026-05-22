# Autonomous Cataloging Agent

An autonomous LLM-powered catalog transformation agent that dynamically converts arbitrary vendor Excel catalogs into a standardized product CSV schema using semantic schema mapping, metadata enrichment, and modular tool orchestration.

---

# Overview

This project implements an intelligent cataloging workflow capable of:

- Reading vendor Excel files with unknown structures
- Dynamically understanding vendor schemas
- Semantically mapping fields to a standardized schema
- Enriching missing attributes using LLM reasoning
- Prioritizing the correct transactional pricing field
- Exporting normalized CSV outputs
- Executing through a stateful autonomous workflow using LangGraph

Unlike traditional ETL pipelines, this system does not rely on hardcoded column mappings or fixed workflows.

When multiple pricing representations exist (e.g., MRP and selling price), the agent intelligently prioritizes the commercially relevant transactional price (`selling_price`) while using MRP as a fallback.

---

# Standardized Output Schema

```csv
sku,name,description,brand,category,color,size,material,price,image_url_1,image_url_2,image_url_3
```

---

# Key Features

## Autonomous Schema Understanding

The agent dynamically interprets arbitrary vendor column structures using LLM reasoning.

Example:

| Vendor Column | Standardized Field |
|---|---|
| selling_price | price |
| main_image_url | image_url_1 |
| image_2 | image_url_2 |

---

## Intelligent Price Resolution

When multiple pricing fields are present, the agent semantically prioritizes:

- `selling_price` → preferred transactional price
- `mrp` → fallback reference price

This mirrors real-world ecommerce catalog normalization behavior.

---

## LLM-Powered Metadata Enrichment

The agent extracts missing attributes such as:

- color
- category
- material

from product names and descriptions.

Example:

```text
Beige Silk Blend Embroidered Festive Wear Kurta Set
```

Extracted:

```json
{
  "color": "Beige",
  "material": "Silk Blend",
  "category": "Kurta Set"
}
```

---

## Stateful Agent Workflow

The system uses LangGraph to orchestrate:

1. Workbook inspection
2. Schema reasoning
3. Product transformation
4. Metadata enrichment
5. CSV export

---

# Architecture

```text
Vendor Excel File
        ↓
Excel Inspection Tool
        ↓
LLM Schema Mapping Agent
        ↓
Price Resolution Logic
        ↓
Product Transformation
        ↓
Attribute Extraction Agent
        ↓
Standardized Product Objects
        ↓
CSV Export
```

---

# Tech Stack

| Component | Technology |
|---|---|
| Language | Python 3.11 |
| Agent Framework | LangGraph |
| LLM Orchestration | LangChain |
| LLM Provider | Groq |
| Model | llama-3.3-70b-versatile |
| Data Processing | Pandas |
| Validation | Pydantic |
| Excel Handling | OpenPyXL |

---

# Project Structure

```text
catalog_agent/
│
├── agents/
│   └── catalog_workflow.py
│
├── tools/
│   ├── inspect_excel.py
│   ├── schema_mapper.py
│   ├── cleaner.py
│   ├── exporter.py
│   └── attribute_extractor.py
│
├── models/
│   └── product_schema.py
│
├── input/
│   └── vendor_catalog.xlsx
│
├── outputs/
│   └── standardized_catalog.csv
│
├── logs/
│   └── agent.log
│
├── main.py
├── requirements.txt
├── README.md
├── .env.example
└── .gitignore
```

---

# Workflow

## 1. Workbook Inspection

The agent inspects:
- sheets
- columns
- sample rows
- missing values

---

## 2. Dynamic Schema Mapping

The LLM semantically maps vendor-specific fields to the target standardized schema.

No hardcoded mappings are used.

---

## 3. Intelligent Price Resolution

If both `selling_price` and `mrp` are available:

- `selling_price` is used as the standardized `price`
- `mrp` is retained as fallback logic

This reflects real-world ecommerce pricing semantics.

---

## 4. Product Transformation

Rows are normalized into structured product objects.

---

## 5. Metadata Enrichment

Missing attributes are inferred using semantic extraction.

---

## 6. CSV Export

The final normalized catalog is exported automatically.

---

# Agentic Behavior

This system was intentionally designed as an autonomous reasoning agent rather than a deterministic ETL pipeline.

The agent:
- interprets unknown schemas
- selects mappings dynamically
- resolves pricing ambiguity intelligently
- enriches incomplete metadata
- orchestrates tool execution through LangGraph

---

# How to Run

## 1. Clone Repository

```bash
git clone <repository_url>
cd catalog_agent
```

---

## 2. Create Virtual Environment

```bash
py -3.11 -m venv venv
```

Activate:

### Windows

```bash
.\venv\Scripts\activate
```

### Linux / Mac

```bash
source venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file:

```env
GROQ_API_KEY=your_groq_api_key
```

---

## 5. Add Vendor Excel File

Place the vendor file inside:

```text
input/
```

Rename it as:

```text
vendor_catalog.xlsx
```

---

## 6. Run the Agent

```bash
python main.py
```

---

# Example Agent Execution

```text
[AGENT] Inspecting workbook...

[AGENT] Generating schema mapping...

[AGENT] Using selling_price as transactional price.

[AGENT] Transforming products...

[AGENT] Exporting standardized catalog...
```

---

# Output

The generated standardized catalog will be available at:

```text
outputs/standardized_catalog.csv
```

---

# Challenges Solved

- Dynamic vendor schemas
- Non-standard column naming
- Multiple pricing representations (MRP vs selling price)
- Missing metadata
- Schema normalization
- Autonomous orchestration
- Structured extraction
- Product enrichment

---

# Future Improvements

- Multi-vendor memory system
- Confidence scoring for mappings
- Multi-sheet intelligent selection
- Image-based enrichment
- OCR support for scanned catalogs
- Human-in-the-loop validation
- Vector database integration
- Async batch processing

---

# Design Philosophy

The system was designed around the principle that vendor catalog structures are inherently non-deterministic.

Instead of building rigid ETL rules, the project implements an adaptive reasoning agent capable of semantic understanding and autonomous transformation.

---

# Author

Sourabh Alimchandani
