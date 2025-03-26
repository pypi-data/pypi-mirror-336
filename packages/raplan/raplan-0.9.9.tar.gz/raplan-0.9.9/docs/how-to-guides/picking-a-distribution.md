# Picking a distribution

## Versatility of Weibull

When in doubt regarding what distribution to pick: we can highly recommend starting off with a
[Weibull distribution][raplan.distributions.Weibull]. It's one of the most versatile distributions
due to its **shape parameter `alpha`**. This shape parameter allows for easy tweaking of the failure
distribution over time, whilst keeping your mean time between failure constant. In fact, by setting
the shape parameter to specific values, the distribution reduces to some other standard distributions!

See the [Weibull distribution Wikipedia page](https://en.wikipedia.org/wiki/Weibull_distribution) for more info.

So let's say:

- your mean time between failure or MTBF is 10 years and you would want to review the **cumulative failure probability**.
- we start at year "0" and look forward 50 years.
- we want to experiment with the shape parameter.
- we want to highlight a threshold where 50% of the components is expected to have failed.

```python
from raplan import Component, Weibull, plot

mtbf = 5
components = [
    Component(
        name=f"Weibull alpha={a}",
        distribution=Weibull(alpha=a, mtbf=mtbf),
    )
    for a in (0.25, 0.5, 1.0, 2.0, 4.0, 10.0, 100.0)
]

# 0.0 - 10.0 in 0.1 steps
xs = list(x / 100.0 for x in range(1001))

fig = plot.get_cfp_figure(components, xs=xs, thresholds={"50%": 0.5})
fig.write_image("./docs/generated/weibull-cfp.svg")
```

<figure markdown>
![Cumulative failure probability of a Weibull distribution.](../generated/weibull-cfp.svg)
<figcaption>
    Cumulative failure probability of a Weibull distribution for different values of shape parameter `alpha`.
</figcaption>
</figure>

Note that even though some distributions appear to fail "faster", their mean time between failure is
all equal to 10 (years) in this case. Their CFP rises quickly initially, but remains relatively
lower the further time progresses to even this out, i.e. components fail fast or just keep ploughing
on.

## Determining or assuming values

Now you still might be guessing what values you should use? The answer is: it depends on a lot of
things! If you don't have any experimental data or datasheets dictating what values to use or
assume, you will have to start by defining what **failure** means in your specific use-case.

Then you can start looking for a suitable shape that corresponds to that failure behavior. A neat
aspect of the [Weibull][raplan.distributions.Weibull] is that the shape parameter `alpha` and the
Mean Time Between Failure `mtbf` are independent such that the shape will simply "stretch out" if
you pick a longer `mtbf`. In general, a low shape `alpha` (>0.0) means more early failures and a
higher alpha results in more failures around the `mtbf`. In case of an extremely high `alpha`, it
approaches a step function around the `mtbf`.
