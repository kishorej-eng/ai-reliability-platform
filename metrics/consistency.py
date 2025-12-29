def consistency_score(outputs: list[str]) -> float:
    """
    Naive consistency metric:
    % of identical outputs across runs.
    """
    if not outputs:
        return 0.0

    unique_outputs = set(outputs)
    return 1.0 / len(unique_outputs)
