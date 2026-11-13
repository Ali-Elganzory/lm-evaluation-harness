from pathlib import Path

import pytest

from lm_eval.tasks._yaml_loader import load_yaml


@pytest.fixture(scope="module")
def task():
    root = Path(__file__).resolve().parents[1]
    return load_yaml(root / "lm_eval/tasks/gpqa/cot_zeroshot/gpqa_diamond_boxed.yaml")


@pytest.mark.parametrize(
    "text, expected",
    [
        (r"\boxed{B}", (1, 1)),
        (r"\boxed{A} earlier. \boxed{\text{(b)}} is final.", (1, 1)),
        (r"<think>\boxed{B}</think>\boxed{C} because of this.", (0, 1)),
        (r"<think>\boxed{B}", (0, 0)),
        (r"\boxed{B}</think>Only prose.", (0, 0)),
        (r"\boxed{B} then \boxed{12}", (0, 0)),
        (r"\boxed{B} then \boxed{C", (0, 0)),
        ("The answer is B.", (0, 0)),
    ],
)
def test_boxed_task_scoring(task, text, expected):
    assert r"\boxed{B}" in task["doc_to_text"]
    result = task["process_results"]({"answer": "(B)"}, [text])
    assert (result["exact_match"], result["format_compliance"]) == expected
