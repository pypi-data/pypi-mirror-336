# RaPlan tutorial

Welcome to the RaPlan tutorial! This page intends to take you through RaPlan's concepts step by step.
Make sure you have RaPlan installed or head to the [Homepage](../README.md) for instructions. RaPlan
is installed on our JupyterLab environments by default.

The tutorial will walk you through the manual creation of a maintenance schedule for a lightbulb. First, it's failure behavior will be modeled using a Weibull distribution. Then we will

## Components: maintenance for what?

Let's start by modeling our maintenance subject: the [`Component`][raplan.Component]! Regardless of
how we will organize things later, it's important to keep in mind that we're trying to keep the
failure of individual components within bounds. What you identify as a component depends on your
application, though in case of RaPlan these are the objects for which you will have to provide the
**failure distribution**.

A [`Component`][raplan.Component] takes the following arguments:

- `name`: Name of the component.
- `age`: Starting age offset (usually in years).
- `distribution`: Failure distribution to use.
- `maintenance`: List of maintenance tasks that should be applied over this component's lifespan.
- `uuid`: Automatically generated unique identifier for this component.

The `name` is there for our own indicative purposes. The `age` indicates how old object is at the
start of our timeline, i.e. its head start in the aging process. The `distribution` is a tricky one!
This is the variable that captures the **failure probability** over time and we'll get into that in
a bit. The `maintenance` is the list of tasks such **maintenance** or **replacement** that will
**rejuvenate** or **reset** the failure distribution.

### Component example: lightbulb

So, lets model a basic lightbulb! We shall name it `"lightbulb"` and assume we own it for 2 years.
Lets assume that our fictional lightbulb has a mean time between failure (MTBF) of 10 years and has
a fairly high probability to fail around that time and a slight probability to do so somewhat sooner
such that we assume an `alpha=4`. You can read more about [picking a distribution in the
corresponding how-to guide](../how-to-guides/picking-a-distribution.md) as well quickly review the
shape of the Weibull curve with respect to the parameter `alpha`.

Without any maintenance, we can use the following snippet to plot the **cumulative failure
probability** of our lightbulb for the next 50 years:

```python
from raplan import Component, Horizon, Weibull, plot

bulb = Component(
    name="lightbulb",
    age=2,
    distribution=Weibull(
        alpha=4,
        mtbf=10,
    ),
)

# A horizon running from 0 to 50 years ahead.
horizon = Horizon(0, 50)
fig = plot.get_cfp_figure(
    bulb,
    # Get ten thousand steps of the appropriate size.
    xs=horizon.get_range(10000),
    horizon=horizon,
)
fig.write_image("./docs/generated/lightbulb-cfp.svg")
```

<figure markdown>
![Cumulative failure probability of a fictional lightbulb.](../generated/lightbulb-cfp.svg)
    <figcaption>
        Cumulative failure probability of a fictional lightbulb with a Weibull failure distribution with `alpha=4` and `mtbf=10`.
    </figcaption>
</figure>

So here we see the default figure that RaPlan outputs for a **cumulative probability distribution**.
That means that the blue line aptly labeled "lightbulb" indicates the probability it will have
failed up until that point in time. Hence it is ever increasing according to the failure
distribution we chose.

By default is also displays a 5% threshold which may seem rather conservative for a lightbulb, but
is commonly used to avoid a lot of corrective maintenance (by things actually failing in production
situations) by doing preventive maintenance.

### Investigating CFP and effective age

You might be interested in the specific _cumulative failure probability_ (CFP) up to a certain point
of time of a component is or what the effective age is at any given time. If you supply a component
with a value for the "time" or `x` in case of RaPlan, you will get the CFP at that point in time,
while taking into account the initial age.

```python
from raplan import Component, Weibull

bulb = Component(
    name="lightbulb",
    age=2,
    distribution=Weibull(
        alpha=4,
        mtbf=10,
    ),
)

assert bulb.get_age_at(0) == 2, "Initial age of 2 at time x=0."
assert round(bulb.cfp(0), ndigits=3) == 0.001, "CFP at effective age of 2."

assert bulb.get_age_at(5) == 7, "Effective age of 7 at time x=5."
assert round(bulb.cfp(5), ndigits=3) == 0.150, "CFP at effective age of 7."
```

Here we can see clearly that without maintenance, the effective age progresses linearly while the
CFP accumulates according to it's Weibull distribution.

## Tasks and Maintenance

So in order to keep our chances of sitting in the dark on the low side, we can attempt to replace
our lightbulbs every now and then! Let's define a `"replace bulb"` [`Task`][raplan.classes.Task]
that symbolizes this. It takes the following arguments:

- `name`: A name to identify this task by.
- `rejuvenation`: Percentage of accumulated age that is won back by executing this task on some
  component.
- `duration`: Duration of the task.
- `cost`: Cost to associate with this task.

```python
from raplan import Task

replace = Task(
    name="replace bulb",
    rejuvenation=1.0,
    duration=1 / 365 / 24,
    cost=1.0,
)
```

This task does a full 100% rejuvenation of the subject, and takes 1 hour to perform on a timescale
of years. We assume that it costs just one unit.

### Replacement

In the grander scheme of things, this task makes sense, but needs **scheduling**. That is where
[`Maintenance`][raplan.classes.Maintenance] comes in. It takes a task and allocates it to a certain
point in time. It takes the following arguments:

- `name`: A name for the maintenance.
- `task`: The task that is executed during this maintenance.
- `time`: The time at which this maintenance takes place. The rejuvenation of a task is currently
  applied at the start of a task.

```python
from raplan import Component, Horizon, Maintenance, Task, Weibull, plot

replace = Task(
    name="replace bulb",
    rejuvenation=1.0,
    duration=1 / 365 / 24,
    cost=1.0,
)

age = 2
period = 4
stock = 10
maintenance = [
    Maintenance(
        name=f"replacement {i}",
        task=replace,
        time=(i + 1) * period,
    )
    for i in range(stock)
]

bulb = Component(
    name="lightbulb",
    age=age,
    distribution=Weibull(
        alpha=4,
        mtbf=10,
    ),
    maintenance=maintenance,
)

assert bulb.get_age_at(4) == 0, "First replacement should reset the age to 0."
assert bulb.get_age_at(5) == 1, "Age should increment regularly from there."

# A horizon running from 0 to 50 years ahead.
horizon = Horizon(0, 50)
fig = plot.get_cfp_figure(
    bulb,
    # Get ten thousand steps of the appropriate size.
    xs=horizon.get_range(10000),
    horizon=horizon,
)
fig.write_image("./docs/generated/lightbulb-replace-cfp.svg")
```

<figure markdown>
![Cumulative failure probability of a fictional lightbulb that is periodically replaced.](../generated/lightbulb-replace-cfp.svg)
    <figcaption>
        Cumulative failure probability of a fictional lightbulb that is periodically replaced.
    </figcaption>
</figure>

Here we apply a periodical replacement maintenance:

- every four years,
- with a stock of 10 bulbs to pick from.

We can clearly see that the stock does not quite lasts through the full forecast horizon
because we approach a 50% cumulative failure probability for our final bulb.

!!! note

    Note how we forgot to take into account the initial age of the lightbulb! Hence the first
    replacement is slightly too late for our level of comfort! We can fix this by offsetting the
    maintenance timing with the initial age:

    `Maintenance(time=(i + 1) * period - age, ...)`

### Rejuvenation

For a lot of components proper maintenance can substantially extend their lifetime. This is modeled
using a **rejuvenation** percentage in RaPlan. Note that a rejuvenation is relative to the age that
the component is at at the time. This means that a 50% rejuvenation when a component is 6 years old
"resets" it's age to 3 years, from where it will start increasing regularly again.

Lets say a good cleaning of our lightbulb's armature:

- happens every 6 months,
- results in a rejuvenation of about 7.5% of the then actual age.

and we want to reduce our replacement period to 10 years to save lightbulbs.

This will result in the following snippet, where we define a `"clean armature"`
[`Task`][raplan.classes.Task] and tweak the [`Maintenance`][raplan.classes.Maintenance] schedule
accordingly:

```python
from raplan import Component, Horizon, Maintenance, Task, Weibull, plot

replace = Task(
    name="replace bulb",
    rejuvenation=1.0,
    duration=1 / 365 / 24,
    cost=1.0,
)
clean = Task(
    name="clean armature",
    rejuvenation=0.075,
    duration=1 / 365 / 2,
    cost=1.0,
)

age = 2
period = 10
stock = 10
replacements = [
    Maintenance(
        name=f"replacement {i}",
        task=replace,
        time=(i + 1) * period - age,
    )
    for i in range(stock)
]

period = 0.5  # 6 months
total = 100
cleanings = [
    Maintenance(name=f"cleaning {i}", task=clean, time=i * period) for i in range(total)
]

bulb = Component(
    name="lightbulb",
    age=age,
    distribution=Weibull(
        alpha=4,
        mtbf=10,
    ),
    maintenance=replacements + cleanings,
)

assert bulb.get_age_at(8) == 0, "First replacement should reset the age to 0."
assert bulb.get_age_at(8.25) == 0.25, "No cleaning, yet."
assert round(bulb.get_age_at(8.5), ndigits=3) == 0.463, "Cleaning reduced some aging!"

# A horizon running from 0 to 50 years ahead.
horizon = Horizon(0, 50)
fig = plot.get_cfp_figure(
    bulb,
    # Get ten thousand steps of the appropriate size.
    xs=horizon.get_range(10000),
    horizon=horizon,
)
fig.write_image("./docs/generated/lightbulb-cleaning-cfp.svg")
```

<figure markdown>
![Cumulative failure probability of a fictional lightbulb that is periodically replaced and cleaned.](../generated/lightbulb-cleaning-cfp.svg)
    <figcaption>
        Cumulative failure probability of a fictional lightbulb that is periodically replaced and cleaned.
    </figcaption>
</figure>

So this looks rather promising! We are now in great shape to let our bulb shine right within our default bounds. But...

!!! note

    Note how the first bulb's failure probability peak right before replacement is still slightly higher than the others.

    Can you guess why this is?

    Our initial bulb's age already sat at 2 years without cleaning, so in a way, that initial age came to bite us again!
    If we **were** cleaning it for the past 2 years already, you can offset and extend the cleanings maintenance, too.

    RaPlan is OK with timings of maintenance that occurred in the past (i.e. are negative). Try it!

!!! note

    This sawtooth pattern is rather typical of maintenance strategies, as maintenance will lengthen the longevity of your
    components quite a bit, but age will catch up with them at some point.

## Systems of components

So far we've modeled a single lightbulb and investigated its failure behavior over time without any
intervention as well as with a replacement and a replacement+cleaning maintenance schedule. However,
what if your subject doesn't consist of a single component, but multiple components instead? In
RaPlan we have dubbed this a [`System`][raplan.classes.System] that consists of multiple
[`Component`][raplan.classes.Component] instances.

### System failure: compound probability

In RaPlan, a system fails if **any** of its components fail. This allows us to review the
**cumulative failure probability** of a system as one (100%) minus the probability that all
components still work. We refer to this as the **compound failure distribution** of the system:

$$
\mathrm{CFP}_{\mathrm{sys}} (t) = 1 - \Pi_{\mathrm{comp} \in \mathbb{C}} (1 - \mathrm{CFP}_{\mathrm{comp}} (t))
$$

Which states that the cumulative failure probability of a system up to a time $t$ is equal to one
minus the product for all components of one minus their failure up to that time (i.e. the probability
they still work). I.e. `1.0 - math.prod(1.0 - p for p in probabilities)` in Python-speak.

### System example: traffic light

Let's come up with an example! Let's investigate a traffic light that for simplicity's sake consists of
three lightbulbs: red, yellow (orange), and green. We pick orange for visualization purposes. We
assume the red light gets the most mileage and has a lower mean time between failure (MTBF) for that
reason. Orange is only transitional most of the time, such that we assume it has the longest
survival probability:

- Weibull shape parameter `alpha` of 4 and
- Red: 10 years,
- Yellow (orange): 20 years, and
- Green: 15 years mean time between failure (MTBF).

We can define a `"traffic light"` [`System`][raplan.classes.System] like so:

```python
from raplan import Component, Horizon, System, Weibull, plot

age = 2
colors = ("red", "orange", "green")
mtbfs = (10, 20, 15)

bulbs = [
    Component(
        name=f"{color} lightbulb",
        age=age,
        distribution=Weibull(
            alpha=4,
            mtbf=mtbf,
        ),
    )
    for color, mtbf in zip(colors, mtbfs)
]

traffic_light = System(
    name="traffic light",
    components=bulbs,
)

# A horizon running from 0 to 50 years ahead.
horizon = Horizon(0, 50)
fig = plot.get_cfp_figure(
    [traffic_light] + bulbs,
    # Get ten thousand steps of the appropriate size.
    xs=horizon.get_range(10000),
    horizon=horizon,
)

# Patch the colors with something intuitive.
for color, trace in zip(colors, fig.data[1:]):
    trace["line_color"] = color

fig.write_image("./docs/generated/traffic_light-cfp.svg")
```

<figure markdown>
![Cumulative failure probability of a traffic light consisting of three separate lightbulbs.](../generated/traffic_light-cfp.svg)
    <figcaption>
        Cumulative failure probability of a traffic light consisting of three separate lightbulbs.
    </figcaption>
</figure>

Here you can see the early failure of the red light dominate the systems probability of failure as
well. This makes sense, as the system's performance is limited by the worst component by definition.
As soon as the red lightbulb's CFP is on the rise, there is little you can do.

## Where to next?

Feel free to check either the [How-to guides](../how-to-guides/README.md) for more specific use
cases, or dive straight into the [Reference](../reference/README.md) for some nicely formatted
reference documentation and get coding!
