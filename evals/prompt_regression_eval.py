import json
from runners.mock_llm import run_llm
from metrics.consistency import consistency_score
from evals.parsers import parse_financial_response

RUNS_PER_PROMPT = 5

def load_dataset(path: str):
    with open(path, "r") as f:
        return json.load(f)

def fill_prompt(template: str, inputs: dict) -> str:
    for key, value in inputs.items():
        template = template.replace(f"{{{{{key}}}}}", value)
    return template

def run_eval():
    dataset = load_dataset("datasets/basic_prompts.json")

    for item in dataset:
        outputs = []

        prompt = fill_prompt(item["prompt"], item["input"])
        

        if item["type"] == "email_summary":
            expected_facts = ["deployment", "failed", "configuration"]

        elif item["type"] == "financial":
            expected_facts = ["revenue", "year", "source"]

        for _ in range(RUNS_PER_PROMPT):
            output = run_llm(prompt)

            # --- Hallucination risk evaluation ---
            try:
                parsed = json.loads(output)
            except json.JSONDecodeError:
                # This itself is a reliability signal
                parsed = None

            if parsed:
                facts_found = sum([
                    parsed.get("mentions_revenue", False),
                    parsed.get("mentions_year", False),
                    parsed.get("source_provided", False)
                ])
            else:
                facts_found = 0

            
            response_lower = output.lower()

            for fact in expected_facts:
                if fact in response_lower:
                    facts_found += 1

            hallucination_risk = 1 - (facts_found / len(expected_facts))
            print(f"Hallucination risk score: {hallucination_risk:.2f}")

            outputs.append(output)

        score = consistency_score(outputs)

        print("=" * 40)
        print(f"Prompt ID: {item['id']}")
        print("Outputs:")
        for o in outputs:
            print("-", o)

        print(f"Consistency score: {score:.2f}")

if __name__ == "__main__":
    run_eval()
