
import json
import re
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "app"))

from assistant import initialise_database, ask_question

CASES_PATH = PROJECT_ROOT / "tests" / "rag_eval_cases.json"


def normalise(text):
    text = text.lower()
    text = re.sub(r"[^\w\s]", " ", text)
    return " ".join(text.split())


def is_abstention(answer):
    answer = normalise(answer)
    phrases = [
        "i don t know",
        "i do not know",
        "not specified",
        "not provided",
        "not available",
        "no information"
    ]
    return any(phrase in answer for phrase in phrases)


def evaluate_case(case, answer):
    if case["should_abstain"]:
        passed = is_abstention(answer)
        missing_facts = []
    else:
        answer_normalised = normalise(answer)
        missing_facts = [
            fact
            for fact in case["expected_facts"]
            if normalise(fact) not in answer_normalised
        ]
        passed = (
            not is_abstention(answer)
            and len(missing_facts) == 0
        )

    return passed, missing_facts


def main():
    cases = json.loads(CASES_PATH.read_text(encoding="utf-8"))
    collection = initialise_database()

    print(f"Running {len(cases)} RAG evaluation cases...")
    print()

    passed_count = 0

    for case in cases:
        print(f"ID: {case['id']}")
        print(f"Question: {case['question']}")

        try:
            result = ask_question(case["question"], collection)
            answer = result["answer"]

            passed, missing_facts = evaluate_case(case, answer)

            if passed:
                passed_count += 1

            print(f"Answer: {answer}")
            print(f"Result: {'PASS' if passed else 'FAIL'}")

            if missing_facts:
                print(f"Missing expected facts: {missing_facts}")

        except Exception as error:
            print(f"Result: ERROR")
            print(f"Error: {error}")

        print("-" * 50)

    score = passed_count / len(cases) * 100 if cases else 0

    print()
    print(f"FINAL SCORE: {passed_count}/{len(cases)} ({score:.1f}%)")


if __name__ == "__main__":
    main()
