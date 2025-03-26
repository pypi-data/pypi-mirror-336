"""Tests for the classes module."""

import inspect

from pytest import raises
from serde import asdict, from_dict, yaml

from raplan import distributions as ds
from raplan.classes import (
    Component,
    CyclicStrategy,
    Horizon,
    Maintenance,
    Project,
    System,
    Task,
)


def test_classes_in_init():
    """Check whether all public classes are imported on the top-level."""
    import raplan as tgt
    from raplan import classes as src

    def spec(obj):
        return inspect.isclass(obj) and obj.__module__ == "raplan.classes"

    src = set(c for _, c in inspect.getmembers(src, spec))
    tgt = set(c for _, c in inspect.getmembers(tgt, spec))
    diff = src.difference(tgt)
    assert not diff


def test_component_roundtrip():
    """Create a component, try to serialize and deserialize it."""

    c = Component()
    ser = yaml.to_yaml(c)
    de: Component = yaml.from_yaml(Component, ser)
    assert de.distribution.cdf() == c.distribution.cdf()
    assert de == c


def test_component():
    """Test component functionality."""
    c = Component(
        name="foo",
        age=100.0,
        maintenance=[
            Maintenance(task=Task(rejuvenation=0.2), time=35),
            Maintenance(task=Task(rejuvenation=0.5), time=10),
        ],
        distribution=ds.Weibull(mtbf=100.0),
    )
    # Test effective age
    assert c.get_age_at(9.0) == 109.0
    assert c.get_age_at(10.0) == 55.0
    assert c.get_age_at(35.0) == 64.0
    assert c.get_age_at(40.5) == 69.5
    # Test cfp, should increment but maintenance should have effect.
    assert c.cfp(9.9) > c.cfp(9.8)
    assert c.cfp(9.9) > c.cfp(10.0)
    assert c.cfp(34.9) > c.cfp(35.0)

    assert c.maintenance[0].end == 36


def test_system_roundtrip():
    """Create a system, try to serialize and deserialize it."""
    s = System()
    ser = yaml.to_yaml(s)
    de: System = yaml.from_yaml(System, ser)
    assert de.cfp() == s.cfp()

    # Also test a dict approach.
    de: System = from_dict(System, dict(uuid=s.uuid))
    assert de == s


def test_system_cfp():
    """Create a system with some components and do some CFP checks."""

    s = System()
    assert s.cfp() == 0.0

    s = System(
        components=[
            Component(name="A", distribution=ds.Uniform(b=10.0)),
            Component(name="B", distribution=ds.Uniform(b=5.0)),
        ]
    )

    ref = 1 - (1 - 0.1) * (1 - 0.2)

    assert s.cfp(-1) == 0.0, "Negative values should always result in 0.0."
    assert s.cfp(0) == 0.0
    assert s.cfp(1) == ref

    s.schedule_maintenance(Maintenance(name="1", task=Task(rejuvenation=1.0), time=1.0))
    s.schedule_maintenance(
        Maintenance(name="100", task=Task(rejuvenation=1.0), time=100.0),
        component="A",
    )
    s.schedule_maintenance(Maintenance(name="20", task=Task(rejuvenation=1.0), time=20.0))
    assert s.cfp(1) == 0.0, "Full repair just happened."
    assert s.cfp(2) == ref, "Value should be offset."

    # Dupes, because both components get the repairs.
    assert [m.name for m in s.get_ordered_maintenance()] == [
        "1",
        "1",
        "20",
        "20",
        "100",
    ]

    with raises(KeyError):
        s.get_component("Foo")


def test_horizon():
    """Tests for Horizon class."""
    h = Horizon()
    with raises(ValueError):
        h.get_range(10)

    h.end = 100
    assert h.get_range(2) == [0.0, 50.0, 100.0]


def test_project():
    """Tests for Project class."""
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
            Component(name="B", distribution=ds.Uniform(b=5)),
        ],
    )

    p = Project()
    assert p.get_horizon_end() == 0.0
    assert p.cfp(100) == 0.0

    p.systems = [s1, s2]
    p.schedule_maintenance(Maintenance(name="1", task=Task(rejuvenation=1.0), time=1.0))
    p.schedule_maintenance(
        Maintenance(name="100", task=Task(rejuvenation=1.0), time=100.0),
        system="1",
        component="A",
    )
    p.schedule_maintenance(
        Maintenance(name="20", task=Task(rejuvenation=1.0), time=20), component="B"
    )

    assert p.get_horizon_end() == 100.0
    p.horizon.end = 20.0
    assert p.get_horizon_end() == 20.0

    assert p.cfp(1) == 1 - (1 - s1.cfp(1)) ** 2
    assert [m.name for m in p.get_ordered_maintenance()] == [
        "1",
        "1",
        "1",
        "1",
        "20",
        "20",
        "100",
    ]

    with raises(KeyError):
        p.get_system("foo")

    sc = p.get_schedule()
    assert len(sc.get_ordered_maintenance()) == len(p.get_ordered_maintenance())

    assert asdict(p), "Should be able to get a dict."


def test_cyclic_strategy():
    h = Horizon(2022, 2042)
    cs = CyclicStrategy(
        tasks=[
            Task("renovate", rejuvenation=0.5),
            Task("conserve", rejuvenation=0.1),
            Task("replace", rejuvenation=1.0),
        ],
        percentages=[
            2 / 3,
            0.25,
            1.0,
        ],  # These are not in order on purpose to check resilience.
    )

    # Check single cycle.
    assert [
        (m.task.name, m.time)
        for m in cs.get_maintenance(age=0, cycle_length=12, horizon=h, repeat=False)
    ] == [("conserve", 3.0), ("renovate", 8.0), ("replace", 12.0)]

    # Check repeat and stop because horizon is only 20 years.
    assert [
        (m.task.name, m.time)
        for m in cs.get_maintenance(age=0, cycle_length=12, horizon=h, repeat=True)
    ] == [
        ("conserve", 3.0),
        ("renovate", 8.0),
        ("replace", 12.0),
        ("conserve", 15.0),
        ("renovate", 20.0),
    ]

    # Check applying to component.
    comp = Component(age=8.0)
    cs.apply_to_component(
        comp,
        cycle_length=12,
        horizon=h,
        repeat=False,
        include_history=True,
        integers=True,
    )
    assert [(m.task.name, m.time) for m in comp.maintenance] == [
        ("conserve", -5),
        ("renovate", 0),
        ("replace", 4),
    ]
    cs.apply_to_component(
        comp,
        cycle_length=12,
        horizon=h,
        repeat=True,
        include_history=True,
        integers=True,
    )
    assert [(m.task.name, m.time) for m in comp.maintenance] == [
        ("conserve", -5),
        ("renovate", 0),
        ("replace", 4),
        ("conserve", 7),
        ("renovate", 12),
        ("replace", 16),
        ("conserve", 19),
    ]
