
from {{PROJECT_SLUG}}.main import main


def test_smoke_sample(tmp_path, monkeypatch) -> None:
    monkeypatch.chdir(tmp_path)
    assert main(["--sample"]) == 0
