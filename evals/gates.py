def reliability_gate(consistency_score: float, hallucination_risk: float):
    reasons = []

    if hallucination_risk > 0.2:
        reasons.append("Hallucination risk too high")

    if consistency_score < 0.7:
        reasons.append("Consistency score too low")

    status = "PASS" if not reasons else "FAIL"
    return status, reasons
