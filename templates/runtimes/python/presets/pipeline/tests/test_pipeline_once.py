
from pathlib import Path

from {{PROJECT_SLUG}}.application.pipeline import run_pipeline


def test_pipeline_writes_output(tmp_path: Path) -> None:
    output = run_pipeline("demo-001", tmp_path)
    assert output.exists()
