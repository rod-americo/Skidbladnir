
from __future__ import annotations

import json
from pathlib import Path
from typing import TypedDict

import pydicom
from pydicom.dataset import FileDataset, FileMetaDataset
from pydicom.uid import (
    ExplicitVRLittleEndian,
    SecondaryCaptureImageStorage,
    generate_uid,
)

from .contracts import StudyManifest


class StudyAccumulator(TypedDict):
    study_instance_uid: str
    accession_number: str
    patient_name: str
    files: list[str]


def iter_dicom_files(inbox: Path) -> list[Path]:
    accepted = {".dcm", ".dicom"}
    return sorted(path for path in inbox.rglob("*") if path.is_file() and path.suffix.lower() in accepted)


def build_study_manifests(inbox: Path) -> list[StudyManifest]:
    grouped: dict[str, StudyAccumulator] = {}

    for dicom_path in iter_dicom_files(inbox):
        dataset = pydicom.dcmread(str(dicom_path), stop_before_pixels=True, force=True)
        study_uid = str(getattr(dataset, "StudyInstanceUID", "") or "unknown-study")
        patient_name = str(getattr(dataset, "PatientName", "") or "").strip()
        accession_number = str(getattr(dataset, "AccessionNumber", "") or "").strip()
        state = grouped.setdefault(
            study_uid,
            {
                "study_instance_uid": study_uid,
                "accession_number": accession_number,
                "patient_name": patient_name,
                "files": [],
            },
        )
        state["files"].append(str(dicom_path))
        if not state["accession_number"] and accession_number:
            state["accession_number"] = accession_number
        if not state["patient_name"] and patient_name:
            state["patient_name"] = patient_name

    manifests = []
    for state in grouped.values():
        files = [str(item) for item in state["files"]]
        manifests.append(
            StudyManifest(
                study_instance_uid=str(state["study_instance_uid"]),
                accession_number=str(state["accession_number"]),
                patient_name=str(state["patient_name"]),
                file_count=len(files),
                files=files,
            )
        )
    return manifests


def write_manifests(manifests: list[StudyManifest], outbox: Path) -> list[Path]:
    outbox.mkdir(parents=True, exist_ok=True)
    written = []
    for manifest in manifests:
        destination = outbox / f"{manifest.study_instance_uid}.json"
        destination.write_text(
            json.dumps(manifest.to_dict(), ensure_ascii=True, indent=2) + "\n",
            encoding="utf-8",
        )
        written.append(destination)
    return written


def run_pipeline(inbox: Path, outbox: Path) -> list[Path]:
    manifests = build_study_manifests(inbox)
    return write_manifests(manifests, outbox)


def write_sample_dicom(inbox: Path) -> Path:
    inbox.mkdir(parents=True, exist_ok=True)
    destination = inbox / "sample.dcm"

    file_meta = FileMetaDataset()
    file_meta.MediaStorageSOPClassUID = SecondaryCaptureImageStorage
    file_meta.MediaStorageSOPInstanceUID = generate_uid()
    file_meta.TransferSyntaxUID = ExplicitVRLittleEndian

    dataset = FileDataset(str(destination), {}, file_meta=file_meta, preamble=b"\0" * 128)
    dataset.PatientName = "SAMPLE^PATIENT"
    dataset.AccessionNumber = "ACC-001"
    dataset.StudyInstanceUID = generate_uid()
    dataset.SeriesInstanceUID = generate_uid()
    dataset.SOPInstanceUID = file_meta.MediaStorageSOPInstanceUID
    dataset.Modality = "OT"
    dataset.save_as(str(destination), enforce_file_format=True)
    return destination
