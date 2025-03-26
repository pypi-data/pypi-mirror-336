"""Dataclasses to use and configure maintenance planning and scheduling with."""

from dataclasses import dataclass
from uuid import UUID, uuid4

from serde import InternalTagging, field, serde

from raplan import distributions

__all__ = [
    "Task",
    "Maintenance",
    "Component",
    "System",
    "Horizon",
    "Procedure",
    "Project",
    "ScheduleItem",
    "Schedule",
    "Procedure",
    "CyclicStrategy",
]


def _is_empty(collection: list | dict | set) -> bool:
    """Check whether a collection is empty."""
    return not collection


@serde(tagging=InternalTagging("type"))
@dataclass
class Task:
    """Maintenance task to apply to a component.

    Arguments:
        name: Name for this action.
        rejuvenation: Rejuvenation factor between [0.0-1.0]. Percentage of age that is
            regained. Therefore, 1.0 would mean a full replacement.
        duration: Duration of the maintenance. Usually in years.
        cost: Cost of the maintenance. Usually expressed in a currency or equivalent.
        uuid: Automatically generated unique identifier for this task.
    """

    name: str | None = field(default=None, skip_if_default=True)
    rejuvenation: int | float = 1.0
    duration: int | float = 1.0
    cost: int | float = 1.0
    uuid: UUID = field(default_factory=uuid4)


@serde(tagging=InternalTagging("type"))
@dataclass
class Maintenance:
    """Maintenance task scheduled at a point in time.

    Arguments:
        name: Name of this maintenance task.
        task: Task information.
        time: Time at which this maintenance is scheduled.
        uuid: Automatically generated unique identifier for this maintenance.
    """

    name: str | None = field(default=None, skip_if_default=True)
    task: Task = field(default_factory=Task)
    time: int | float = 1.0
    uuid: UUID = field(default_factory=uuid4)

    @property
    def end(self) -> int | float:
        """End time of this maintenance."""
        return self.time + self.task.duration

    def get_progress(self, x: int | float) -> float:
        """Percentage of the set task that is completed at a given time."""
        if x < self.time:
            return 0.0
        elif x >= self.end or self.task.duration == 0:
            return 1.0
        else:
            return min(1.0, (x - self.time) / self.task.duration)


@serde(tagging=InternalTagging("type"))
@dataclass
class Component:
    """Component with a failure distribution.

    Arguments:
        name: Name of this component.
        age: Starting age offset (usually in years).
        distribution: Failure distribution to use.
        maintenance: List of maintenance tasks that should be applied over this
            component's lifespan.
        uuid: Automatically generated unique identifier for this component.
    """

    name: str | None = field(default=None, skip_if_default=True)
    age: int | float = 0.0
    lifetime: int | float = 1.0
    distribution: distributions.Distributions = field(default_factory=distributions.Weibull)
    maintenance: list[Maintenance] = field(default_factory=list, skip_if=_is_empty, repr=False)
    uuid: UUID = field(default_factory=uuid4)

    def get_ordered_maintenance(self) -> list[Maintenance]:
        """Maintenance tasks sorted in time."""
        return sorted(self.maintenance, key=lambda m: m.time)

    def cfp(self, x: int | float = 1.0) -> float:
        """Cumulative failure probability density function incorporating maintenance."""
        return self.distribution.cdf(self.get_age_at(x))

    def get_age_at(self, x: int | float = 1.0) -> float:
        """Effective age at a point in time given the currently set schedule."""
        age = float(self.age)
        last_time = 0.0
        for m in self.get_ordered_maintenance():
            if m.time > x:
                # Maintenance is yet to happen.
                break
            # Apply rejuvenation with the then actual age.
            age = (age + m.time - last_time) * (1.0 - m.task.rejuvenation)
            last_time = m.time
        # Add remaining time since last maintenance.
        age += x - last_time
        return age

    def schedule_maintenance(self, maintenance: Maintenance):
        """Schedule maintenance for a single or all system's component or all
        components.

        Arguments:
            maintenance: Maintenance to schedule.
        """
        self.maintenance.append(maintenance)


@serde(tagging=InternalTagging("type"))
@dataclass
class System:
    """A system consisting of multiple components.

    Arguments:
        name: Name of this system.
        components: Components of this system.
        uuid: Automatically generated unique identifier for this system.
    """

    name: str | None = field(default=None, skip_if_default=True)
    components: list[Component] = field(default_factory=list, skip_if=_is_empty, repr=False)
    uuid: UUID = field(default_factory=uuid4)

    def cfp(self, x: int | float = 1.0) -> float:
        """Cumulative failure probability density function as the sum of its
        components' respective function incorporating maintenance.
        """
        if len(self.components):
            return distributions.compound_probability(c.cfp(x) for c in self.components)
        else:
            return 0.0

    def get_ordered_maintenance(self) -> list[Maintenance]:
        """Get all maintenance ordered in time."""
        return sorted([m for c in self.components for m in c.maintenance], key=lambda m: m.time)

    def get_component(self, name: str) -> Component:
        """Get a component by name."""
        for c in self.components:
            if c.name == name:
                return c
        raise KeyError(f"Component with name '{name}' does not exist in this system.")

    def schedule_maintenance(self, maintenance: Maintenance, component: str | None = None):
        """Schedule maintenance for a single or all system's component or all
        components.

        Arguments:
            maintenance: Maintenance to schedule.
            component: Component name. If kept `None`, it will be applied to all.
        """
        if component is None:
            for c in self.components:
                c.schedule_maintenance(maintenance)
        else:
            self.get_component(component).schedule_maintenance(maintenance)


@serde(tagging=InternalTagging("type"))
@dataclass
class Horizon:
    """Maintenance planning and scheduling horizon.

    Arguments:
        start: Start of the planning horizon.
        end: End of the planning horizon. Optional, as it is otherwise derived from the
            final task in the schedule.
        uuid: Automatically generated unique identifier for this Horizon.
    """

    start: int | float = 0.0
    end: int | float | None = field(default=None, skip_if_default=True)
    uuid: UUID = field(default_factory=uuid4)

    def get_range(self, steps: int, zero_based: bool = True) -> list[int | float]:
        """Range between start and end (inclusive) in the given number of steps."""
        if self.end is None:
            raise ValueError("Can't calculate a range with no horizon end value.")
        step_size = (self.end - self.start) / steps
        start = type(self.start)(0) if zero_based else self.start
        return [start + i * step_size for i in range(steps + 1)]


@serde(tagging=InternalTagging("type"))
@dataclass
class Project:
    """Maintenance planning and scheduling project.

    Arguments:
        name: Optional name to identify this project by.
        horizon: Timescale horizon for this project. What timeframe are we looking at?
        systems: List of systems to consider a part of this maintenance project.
        uuid: Automatically generated unique identifier for this project.
    """

    name: str | None = field(default=None, skip_if_default=True)
    horizon: Horizon = field(default_factory=Horizon)
    systems: list[System] = field(default_factory=list, skip_if=_is_empty, repr=False)
    uuid: UUID = field(default_factory=uuid4)

    def get_horizon_end(self) -> float:
        """Get the end of the planning horizon or last maintenance task."""
        if self.horizon.end is None:
            end = 0.0
            try:
                end = max(m.time for s in self.systems for c in s.components for m in c.maintenance)
            except ValueError:
                pass  # arg is an empty sequency: end = 0.0
            finally:
                return end
        return self.horizon.end

    def cfp(self, x: int | float = 1.0) -> float:
        """Cumulative failure probability density function as the sum of its
        systems' respective function incorporating maintenance.
        """
        if len(self.systems):
            return distributions.compound_probability(s.cfp(x) for s in self.systems)
        else:
            return 0.0

    def get_ordered_maintenance(self) -> list[Maintenance]:
        """Get all maintenance ordered in time."""
        return sorted(
            [m for s in self.systems for c in s.components for m in c.maintenance],
            key=lambda m: m.time,
        )

    def get_system(self, name: str) -> System:
        """Get a component by name."""
        for s in self.systems:
            if s.name == name:
                return s
        raise KeyError(f"System with name '{name}' does not exist in this project.")

    def schedule_maintenance(
        self,
        maintenance: Maintenance,
        system: str | None = None,
        component: str | None = None,
    ):
        """Schedule maintenance for a single or all system's component or all
        components.

        Arguments:
            maintenance: Maintenance to schedule.
            system: System name. If kept `None`, it will be applied to all.
            component: Component name. If kept `None`, it will be applied to all.
        """
        if system is None:
            for s in self.systems:
                s.schedule_maintenance(maintenance, component=component)
        else:
            self.get_system(system).schedule_maintenance(maintenance, component=component)

    def get_schedule(self) -> "Schedule":
        """Get a fully generated schedule."""
        return Schedule(
            items=[
                ScheduleItem(
                    name=m.task.name,
                    project=self.name,
                    system=s.name,
                    component=c.name,
                    maintenance=m.name,
                    task=m.task.name,
                    rejuvenation=m.task.rejuvenation,
                    duration=m.task.duration,
                    cost=m.task.cost,
                    time=m.time,
                )
                for s in self.systems
                for c in s.components
                for m in c.maintenance
            ]
        )


@serde(tagging=InternalTagging("type"))
@dataclass
class ScheduleItem:
    """A schedule item with full detail regarding its system, component and maintenance
    task info.

    Arguments:
        name: Name for this action.
        project: Name of the project this item belongs to if any.
        system: Name of the system to which this maintenance is applied.
        component: Name of the component to which this maintenance is applied.
        maintenance: Name of the maintenance schedule this item belongs to if any.
        rejuvenation: Rejuvenation factor between [0.0-1.0].
            Percentage of age that is regained. Therefore, 1.0 would mean a full replacement.
        duration: Duration of the maintenance. Usually in years.
        cost: Cost of the maintenance. Usually expressed in a currency or equivalent.
        time: Time at which this maintenance is scheduled.
        uuid: Automatically generated unique identifier for this schedule item.
    """

    name: str | None = field(default=None, skip_if_default=True)
    project: str | None = field(default=None, skip_if_default=True)
    system: str | None = field(default=None, skip_if_default=True)
    component: str | None = field(default=None, skip_if_default=True)
    maintenance: str | None = field(default=None, skip_if_default=True)
    task: str | None = field(default=None, skip_if_default=True)
    rejuvenation: int | float = 1.0
    duration: int | float = 1.0
    cost: int | float = 1.0
    time: int | float = 1.0
    uuid: UUID = field(default_factory=uuid4)


@serde(tagging=InternalTagging("type"))
@dataclass
class Schedule:
    """A full maintenance schedule.

    Arguments:
        items: Scheduled tasks.
        uuid: Automatically generated unique identifier for this maintenance schedule.
    """

    items: list[ScheduleItem] = field(default_factory=list, skip_if=_is_empty)
    uuid: UUID = field(default_factory=uuid4)

    def get_ordered_maintenance(self) -> list[ScheduleItem]:
        """Get all tasks ordered in time."""
        return sorted(self.items, key=lambda t: t.time)

    @classmethod
    def from_projects(cls, projects: list[Project]) -> "Schedule":
        """Create a schedule for multiple projects."""

        schedules = [p.get_schedule() for p in projects]
        return cls(items=[i for s in schedules for i in s.items])


@serde(tagging=InternalTagging("type"))
@dataclass
class Procedure:
    """A specific grouping of tasks to apply to a System.

    Note:
        Mainly used for plotting purposes.

    Arguments:
        name: Name for this procedure.
        system: System (name) to which the procedure should be applied.
        kind: Kind of procedure (category name).
        time: Time at which the procedure is scheduled.
        cost: Cost of the procedure.
        duration: Duration of the procedure.
        uuid: Automatically generated unique identifier for this procedure.
    """

    name: str | None = field(default=None, skip_if_default=True)
    system: str = "system"
    kind: str = "procedure"
    time: int | float = 1.0
    cost: int | float = 1.0
    duration: int | float = 1.0
    uuid: UUID = field(default_factory=uuid4)


@serde(tagging=InternalTagging("type"))
@dataclass
class CyclicStrategy:
    """Maintenance strategy to renovate or replace a component at certain percentages
    of a cycle.

    Arguments:
        name: Name for this cyclic strategy.
        tasks: List of tasks that should be applied at the corresponding entry in percentages.
        percentages: List of percentages [0.0, 1.0] at which to apply tasks.
        uuid: Automatically generated unique identifier for this cyclic strategy.
    """

    name: str | None = field(default=None, skip_if_default=True)
    tasks: list[Task] = field(default_factory=list, skip_if=_is_empty)
    percentages: list[float] = field(default_factory=list, skip_if=_is_empty)
    uuid: UUID = field(default_factory=uuid4)

    def __post_init__(self) -> None:
        assert len(self.tasks) == len(self.percentages), (
            "The number of tasks and percentages should be equal."
        )

    def apply_to_component(
        self,
        component: Component,
        cycle_length: int | float,
        horizon: Horizon,
        repeat: bool = True,
        include_history: bool = True,
        integers: bool = False,
        overwrite: bool = True,
    ) -> None:
        """Apply this strategy to a component.

        Arguments:
            component: Component for which to schedule maintenance.
            cycle_length: Cycle length.
            horizon: Planning horizon to consider.
            repeat: Whether the cycle should be repeated until the end of the horizon.
            include_history: Whether to include historical maintenance entries for
                components that have a pre-defined age.
            overwrite: Whether to fully overwrite a component's maintenance planning
                with this new one or extend it.
            integers: Whether to force all times to be integers.
        """
        maintenance = self.get_maintenance(
            component.age,
            cycle_length,
            horizon,
            repeat=repeat,
            include_history=include_history,
            integers=integers,
            prefix=component.name,
        )
        if overwrite:
            component.maintenance = maintenance
        else:
            component.maintenance.extend(maintenance)

    def get_maintenance(
        self,
        age: int | float,
        cycle_length: int | float,
        horizon: Horizon,
        prefix: str | None = None,
        repeat: bool = True,
        include_history: bool = True,
        integers: bool = False,
    ) -> list[Maintenance]:
        """Get maintenance list for this strategy.

        Arguments:
            age: Starting age of a virtual component.
            cycle_length: Cycle length.
            horizon: Planning horizon to consider.
            prefix: Maintenance naming prefix.
            repeat: Whether the cycle should be repeated until the end of the horizon.
            include_history: Whether to include historical maintenance entries for
                components that have a pre-defined age.
            integers: Whether to force all times to be integers.

        Returns:
            Maintenance list.
        """

        start: int | float = -age
        end = horizon.end - horizon.start if horizon.end else cycle_length

        offsets = [p * cycle_length for p in self.percentages]
        tasks = sorted(zip(offsets, self.tasks), key=lambda x: x[0])
        n_tasks = len(tasks)

        maintenance = []
        cycles_offset: int | float = 0
        while start + cycles_offset < end:
            for index, (offset, task) in enumerate(tasks):
                time = offset + cycles_offset + start
                if integers:
                    time = round(time)

                # No further planning beyond this point.
                if time > end:
                    break

                if not include_history and time < 0:
                    continue

                _prefix = f"{prefix} | " if prefix else ""
                _name = f"{self.name} | " if self.name else ""

                maintenance.append(
                    Maintenance(
                        f"{_prefix}{_name}{index + 1}/{n_tasks} | {task.name} @ {time}",
                        task=task,
                        time=time,
                    )
                )

            # No further planning beyond this point.
            if not repeat or time > end:
                break

            cycles_offset = cycles_offset + cycle_length

        return maintenance
