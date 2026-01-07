import sys
import json
from runners.mock_llm import run_llm
from metrics.consistency import consistency_score
from evals.parsers import parse_financial_response
from evals.gates import reliability_gate
from evals.attribution import attribute_failure
from evals.drift import detect_drift
from evals.history import load_baseline


def load_dataset(path: str):
    with open(path, "r") as f:
        return json.load(f)


dataset = load_dataset("datasets/basic_prompts.json")
print(dataset)
