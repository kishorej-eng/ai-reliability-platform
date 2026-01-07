def attribute_failure(
    task_type: str,
    consistency_score: float,
    hallucination_risk: float,
    parsed_ok: bool
):
    reasons = []

    if not parsed_ok:
        reasons.append("FORMAT_VIOLATION")

    if consistency_score < 0.6:
        reasons.append("INCONSISTENT_OUTPUTS")

    if hallucination_risk > 0.3:
        if task_type == "financial":
            reasons.append("FACTUAL_MISMATCH")
        else:
            reasons.append("MISSING_KEY_FACTS")

    return reasons


