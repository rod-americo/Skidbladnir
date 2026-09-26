
import json

from {{PROJECT_SLUG}}.application.pipeline import run_pipeline, write_sample_dicom


def test_dicom_pipeline_writes_manifest(tmp_path) -> None:
    inbox = tmp_path / "inbox"
    outbox = tmp_path / "outbox"
    write_sample_dicom(inbox)
    outputs = run_pipeline(inbox, outbox)
    assert len(outputs) == 1
    payload = json.loads(outputs[0].read_text(encoding="utf-8"))
    assert payload["file_count"] == 1
    assert payload["study_instance_uid"]
