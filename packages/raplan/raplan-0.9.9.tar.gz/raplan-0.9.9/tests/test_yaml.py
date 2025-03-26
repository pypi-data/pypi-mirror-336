"""Tests for the I/O module."""

from raplan.classes import Project
from raplan.yaml import from_yaml, to_yaml


def test_roundtrip(tmpdir, proj):
    fpath = tmpdir / "project.yml"
    to_yaml(proj, fpath)
    roundtrip = from_yaml(Project, fpath)
    assert roundtrip == proj
