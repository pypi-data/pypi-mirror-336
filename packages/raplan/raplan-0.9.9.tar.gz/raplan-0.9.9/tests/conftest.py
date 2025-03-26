"""Test config for RaPlan."""

from pathlib import Path
from random import random, seed

from pytest import fixture
from ragraph.graph import Graph

from raplan import distributions as ds
from raplan.classes import (
    Component,
    Horizon,
    Maintenance,
    Procedure,
    Project,
    System,
    Task,
)

HERE = Path(__file__).parent


@fixture
def here() -> Path:
    return HERE


@fixture
def data_dir() -> Path:
    return HERE / "data"


@fixture
def docs_dir() -> Path:
    return HERE.parent / "docs"


@fixture
def docs_generated(docs_dir: Path) -> Path:
    path = docs_dir / "generated"
    path.mkdir(exist_ok=True)
    return path


@fixture
def proj() -> Project:
    s1 = System(
        name="1",
        components=[
            Component(name="A", distribution=ds.Uniform(b=10.0)),
            Component(name="B", distribution=ds.Uniform(b=5.0)),
        ],
    )
    s2 = System(
        name="2",
        components=[
            Component(name="A", distribution=ds.Uniform(b=10.0)),
            Component(name="B", distribution=ds.Uniform(b=5.0)),
        ],
    )

    p = Project(systems=[s1, s2], horizon=Horizon(end=100.0))
    p.schedule_maintenance(Maintenance(name="1", task=Task(rejuvenation=1.0), time=1.0))
    p.schedule_maintenance(
        Maintenance(name="100", task=Task(rejuvenation=1.0), time=100.0),
        system="1",
        component="A",
    )
    p.schedule_maintenance(
        Maintenance(name="20", task=Task(rejuvenation=1.0), time=20.0), component="B"
    )

    return p


@fixture
def mgraph(proj: Project) -> Graph:
    """A maintenance graph of the proj fixture."""
    from raplan.analysis import get_maintenance_graph

    return get_maintenance_graph(proj, 20.0)


@fixture
def procedures() -> list[Procedure]:
    """A list of procedures."""
    seed(0)
    xs = list(range(2022, 2053))

    n_objects = 5
    objects = [f"O{i}" for i in range(n_objects)]

    n_kinds = 3
    kinds = [f"type {i}" for i in range(n_kinds)]
    kind_threshold = 1 / n_kinds

    density = 0.25  # Random density for each object's events.
    procedures = []
    for obj in objects:
        for time in xs:
            if random() > density:
                continue
            kind_num = int(random() // kind_threshold)
            kind = kinds[kind_num]
            procedures.append(
                Procedure(
                    name=f"{obj}-{kind}",
                    system=obj,
                    kind=kind,
                    time=time,
                    cost=min((random() // 0.25 + 1) * 0.25, 1.0),
                    duration=min((random() // 0.25 + 1) * 0.25, 1.0),
                )
            )
    return procedures
