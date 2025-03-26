# Introduction

Welcome to RaPlan's documentation! RaPlan is a library to facilitate maintenance planning and
scheduling in Python. In this documentation you can find:

1. [Tutorial](./tutorial/README.md) for step-by-step educational content,
1. [How-to guides](./how-to-guides/README.md) for a more use-case centric approach,
1. The package's [Reference](./reference/README.md) of all classes and functions including source code,
1. Some [Explanation](./explanation/README.md) and rationale behind the library,
1. The [Changelog](./CHANGELOG.md) outlining all changes following the
   [https://keepachangelog.com](https://keepachangelog.com) conventions.

# Installation instructions

RaPlan is installable via pip or your favorite Python dependency manager from PyPI.
If you want all the goods, you can get going with:

```bash
pip install raplan[all]
```

or for instance for Poetry:

```bash
poetry add raplan -E all
```

or `uv`:

```bash
uv add raplan[all]
```

For a development installation, clone the repository and do a `just install`.

# License and contributions

For contribution instructions, head over to the
[open-source GitLab repository](https://gitlab.com/ratio-case-os/python/ragraph)!

All code snippets in the tutorial and how-to guide sections of this documentation are free to use.

If you find any documentation worthwhile citing, please do so with a proper reference to our
documentation!

RaPlan is licensed following a dual licensing model. In short, we want to provide anyone that
wishes to use our published software under the GNU GPLv3 to do so freely and without any further
limitation. The GNU GPLv3 is a strong copyleft license that promotes the distribution of free,
open-source software. In that spirit, it requires dependent pieces of software to follow the same
route. This might be too restrictive for some. To accommodate users with specific requirements
regarding licenses, we offer a proprietary license. The terms can be discussed by reaching out to
Ratio.
