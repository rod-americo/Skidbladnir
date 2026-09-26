
from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class StudyManifest:
    study_instance_uid: str
    accession_number: str
    patient_name: str
    file_count: int
    files: list[str]

    def to_dict(self) -> dict[str, object]:
        return asdict(self)
