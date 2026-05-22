from agents.catalog_workflow import catalog_agent


initial_state = {
    "file_path": "input/vendor_catalog.xlsx",
    "inspection": {},
    "columns": [],
    "mapping": {},
    "dataframe": None,
    "products": []
}


catalog_agent.invoke(initial_state)

print("\nCatalog Agent Execution Completed.")