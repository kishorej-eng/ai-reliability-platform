import json


def parse_financial_response(output: str):
    """
    Attempts to parse model output as JSON.
    Returns dict if valid, else None.
    """
    try:
        return json.loads(output)
    except json.JSONDecodeError:
        return None
