"""Tests for the plot module."""

from pathlib import Path

from raplan import Horizon, Procedure, Project, plot


def test_plot(proj: Project, tmpdir: Path):
    """Basic plotting smoke tests."""

    xs = proj.horizon.get_range(100)
    for i, fig in enumerate(
        [
            plot.get_cfp_figure(
                proj.systems, xs=xs, compound="Project", horizon=Horizon(-100, None)
            ),
            plot.get_cost_figure(proj.systems, horizon=Horizon(-100, None)),
            plot.get_duration_figure(proj.systems, horizon=Horizon(2022, None)),
            plot.get_overview_figure(proj, xs=xs),
            plot.get_overview_figure(
                proj.systems, xs=xs, compound="Project", horizon=Horizon(2022, 2025)
            ),
        ]
    ):
        fig.write_image(tmpdir / f"{i}.svg", format="svg")
        fig.write_html(tmpdir / f"{i}.html")


def test_procedures_plot(procedures: list[Procedure], tmpdir: Path):
    """Test a procedures plot."""
    fig = plot.get_procedures_plot(procedures)
    fig.write_image(tmpdir / "procedures.svg", format="svg")
    fig.write_html(tmpdir / "procedures.html")
