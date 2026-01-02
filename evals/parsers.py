import json
from jsonschema import validate, ValidationError
from evals.schemas import FINANCIAL_SCHEMA


def parse_financial_response(output: str):
    try:
        parsed = json.loads(output)
        validate(instance=parsed, schema=FINANCIAL_SCHEMA)
        return parsed
    except (json.JSONDecodeError, ValidationError):
        return None
