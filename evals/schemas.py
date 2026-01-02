FINANCIAL_SCHEMA = {
    "type": "object",
    "required": ["revenue", "year", "source"],
    "properties": {
        "revenue": {"type": "number"},
        "year": {"type": "number"},
        "source": {"type": "string"}
    }
}
