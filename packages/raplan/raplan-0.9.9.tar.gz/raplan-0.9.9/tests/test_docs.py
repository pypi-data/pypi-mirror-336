from pathlib import Path

import pytest
from pytest_examples import CodeExample, EvalExample, find_examples

DOCS_DIR = Path(__file__).parent.parent / "docs"
DOCS_FILES = DOCS_DIR.glob("**/*.md")


@pytest.mark.parametrize("example", find_examples(*DOCS_FILES), ids=str)
def test_docs(example: CodeExample, eval_example: EvalExample, docs_dir, docs_generated):
    """Test the package's documentation."""
    globals = dict(docs_dir=docs_dir, docs_generated=docs_generated)
    eval_example.set_config(line_length=88, target_version="py311", isort=True)
    if eval_example.update_examples:
        eval_example.format(example)
        eval_example.run_print_update(example, module_globals=globals)
    else:
        eval_example.lint(example)
        eval_example.run_print_check(example, module_globals=globals)
