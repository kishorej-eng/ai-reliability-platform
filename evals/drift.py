def detect_drift(
    prompt_id: str,
    current_consistency: float,
    current_hallucination: float,
    baseline: dict,
    tolerance: dict = None
):
    tolerance = tolerance or {
        "consistency_drop": 0.15,
        "hallucination_increase": 0.15
    }

    expected = baseline.get(prompt_id)

    if not expected:
        return "UNKNOWN", ["No baseline available"]

    reasons = []

    if current_consistency < expected["consistency_score"] - tolerance["consistency_drop"]:
        reasons.append("CONSISTENCY_DRIFT")

    if current_hallucination > expected["hallucination_risk"] + tolerance["hallucination_increase"]:
        reasons.append("HALLUCINATION_DRIFT")

    if reasons:
        return "DRIFT_DETECTED", reasons

    return "STABLE", []


