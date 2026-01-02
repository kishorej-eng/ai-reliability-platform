import json
from runners.mock_llm import run_llm
from metrics.consistency import consistency_score
from evals.parsers import parse_financial_response
from evals.gates import reliability_gate

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
        hallucination_risks = []

        prompt = fill_prompt(item["prompt"], item["input"])
        

        if item["type"] == "email_summary":
            expected_facts = ["deployment", "failed", "configuration"]

        
        for _ in range(RUNS_PER_PROMPT):
            output = run_llm(prompt)

            # --- Hallucination risk evaluation ---
            
                        
            if item["type"] == "financial":
                parsed = parse_financial_response(output)

                if not parsed:
                    hallucination_risk = 1.0
                else:
                    gt = item["ground_truth"]
                    mismatches = sum([
                        parsed["revenue"] != gt["revenue"],
                        parsed["year"] != gt["year"],
                        parsed["source"] != gt["source"]
                    ])
                    hallucination_risk = mismatches / 3

            elif item["type"] == "email_summary":
                response_lower = output.lower()
                facts_found = sum(1 for f in expected_facts if f in response_lower)
                hallucination_risk = 1 - (facts_found / len(expected_facts))
            else:
                hallucination_risk = 1.0  # unknown task type

            print(f"Hallucination risk score: {hallucination_risk:.2f}")
            
            hallucination_risks.append(hallucination_risk)
            outputs.append(output)

        avg_hallucination_risk = sum(hallucination_risks) / len(hallucination_risks)
        
        score = consistency_score(outputs)

        status, reasons = reliability_gate(
            consistency_score=score,
            hallucination_risk=avg_hallucination_risk
        )
        

        print("=" * 40)
        print(f"Prompt ID: {item['id']}")
        print("Outputs:")
        for o in outputs:
            print("-", o)

        print(f"Consistency score: {score:.2f}")
        print(f"RELIABILITY GATE: {status}")
        for r in reasons:
            print(" -", r)

if __name__ == "__main__":
    run_eval()
