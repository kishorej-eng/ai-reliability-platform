import sys
import json
from datetime import datetime

from runners.mock_llm import run_llm
from metrics.consistency import consistency_score
from evals.parsers import parse_financial_response
from evals.gates import reliability_gate
from evals.attribution import attribute_failure
from evals.drift import detect_drift
from evals.history import load_baseline, save_result, save_baseline

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
    baseline = load_baseline("baselines/prompt_baseline.json")

    overall_status = "PASS"

    for item in dataset:
        outputs = []
        hallucination_risks = []
        parsed_ok_overall = True

        prompt = fill_prompt(item["prompt"], item["input"])

        if item["type"] == "email_summary":
            expected_facts = ["deployment", "failed", "configuration"]

        for _ in range(RUNS_PER_PROMPT):
            output = run_llm(prompt)

            if item["type"] == "financial":
                parsed = parse_financial_response(output)

                if not parsed:
                    hallucination_risk = 1.0
                    parsed_ok_overall = False
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
                hallucination_risk = 1.0

            hallucination_risks.append(hallucination_risk)
            outputs.append(output)

        avg_hallucination_risk = sum(hallucination_risks) / len(hallucination_risks)
        score = consistency_score(outputs)

        status, _ = reliability_gate(
            consistency_score=score,
            hallucination_risk=avg_hallucination_risk
        )

        drift_status, _ = detect_drift(
            prompt_id=item["id"],
            current_consistency=score,
            current_hallucination=avg_hallucination_risk,
            baseline=baseline
        )

        failure_reasons = []

        if status == "FAIL":
            overall_status = "FAIL"
            failure_reasons = attribute_failure(
                task_type=item["type"],
                consistency_score=score,
                hallucination_risk=avg_hallucination_risk,
                parsed_ok=parsed_ok_overall
            )

        eval_result = {
            "prompt_id": item["id"],
            "task_type": item["type"],
            "consistency_score": round(score, 2),
            "avg_hallucination_risk": round(avg_hallucination_risk, 2),
            "reliability_status": status,
            "failure_reasons": failure_reasons,
            "drift_status": drift_status,
            "timestamp": datetime.utcnow().isoformat()
        }

        save_result(eval_result)

        if status == "PASS":
            save_baseline(eval_result)

        print("=" * 40)
        print(json.dumps(eval_result, indent=2))

    if overall_status == "FAIL":
        print("\n[Error] Evaluation failed")
        sys.exit(1)
    else:
        print("\n[OK] Evaluation passed")
        sys.exit(0)


if __name__ == "__main__":
    run_eval()
