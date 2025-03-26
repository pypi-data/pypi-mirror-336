"""Tests for the Excel I/O module."""

from pathlib import Path

from raplan import Project, excel


def test_excel_roundtrip(proj: Project, tmp_path: Path):
    path = tmp_path / "export.xlsx"
    excel.to_excel(proj, path)
    de = excel.from_excel(path)
    assert proj == de


def test_yaml_to_excel(data_dir: Path, tmp_path: Path):
    from serde.yaml import from_yaml

    proj = from_yaml(Project, (data_dir / "project.yml").read_text())
    excel.to_excel(proj, tmp_path / "project.xlsx")
