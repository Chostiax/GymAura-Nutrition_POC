from pprint import pprint

from src.data_prep import load_and_prepare_dataset
from src.pipeline import run_pipeline
from src.evaluation import evaluate_pipeline
from tests.test_cases import TEST_CASES

"""
Main entry point for the nutrition PoC.

Flow:
1. Load and clean the USDA-based dataset
2. Run one manual demo sentence
3. Evaluate the full pipeline on the benchmark test set
"""

DATA_PATH = "data/food_item_rows.csv"


def show_single_demo(dataset):
    """
    Quick manual demo before running the full evaluation.
    """
    text = "I had some cereals with oat milk and some coffee"
    result = run_pipeline(text, dataset)

    print("\n" + "=" * 60)
    print("SINGLE DEMO")
    print("=" * 60)
    pprint(result)


def show_evaluation(dataset):
    """
    Run the full KPI evaluation on the 29 test sentences.
    """
    evaluation = evaluate_pipeline(TEST_CASES, dataset)

    print("\n" + "=" * 60)
    print("EVALUATION METRICS")
    print("=" * 60)
    pprint(evaluation["metrics"])

    print("\n" + "=" * 60)
    print("PER-CASE EVALUATION RESULTS")
    print("=" * 60)
    for i, case in enumerate(evaluation["details"], start=1):
        status = "PASS" if (case["all_detected"] and case["all_matched"]) else "FAIL/PARTIAL"
        print(f"\n[{i}/29] {status}")
        print(f"Input: {case['input']}")
        print(f"Expected: {case['expected']}")
        pprint(case["result"])

def main():
    print("Loading dataset...")
    dataset = load_and_prepare_dataset(DATA_PATH)
    print(f"Loaded {len(dataset)} usable dataset rows.")

    show_single_demo(dataset)
    show_evaluation(dataset)


if __name__ == "__main__":
    main()