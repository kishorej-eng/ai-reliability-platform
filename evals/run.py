import sys
from evals.prompt_regression_eval import run_eval

def main():
    status = run_eval()

    if status != "PASS":
        print("❌ Reliability gate failed. Blocking deployment.")
        sys.exit(1)

    print("✅ Reliability gate passed.")
    sys.exit(0)

if __name__ == "__main__":
    main()

