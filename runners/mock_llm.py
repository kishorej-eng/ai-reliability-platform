import random

RESPONSES = [
    "The deployment failed due to a configuration issue and is being rolled back.",
    "A config issue caused the deployment failure, and the team is rolling back.",
    "The production deployment failed because of configuration problems."
]

def run_llm(prompt: str) -> str:
    """
    Simulates non-deterministic LLM behavior.
    """
    return random.choice(RESPONSES)
