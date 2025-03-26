"""Tests for the analysis module."""

from raplan import Project, analysis


def test_get_graph(proj: Project):
    """Test the graph creation."""

    g = analysis.get_maintenance_graph(proj, 20)
    assert len(g.nodes) == 9
    assert len(g.edges) == 38
