# tests

    julia/runtests.jl      entry point for Julia tests
    python/                pytest tests

    make test              runs every language present; skips an absent one, loudly

## The test that matters most

At least one test per topic is a **known-answer test of the full chain**: a problem with an
exact closed-form solution, run through the same assembly → solve → refinement → acceptance
path the real solver uses, in every precision tier the project uses.

Unit tests of each piece are necessary and not sufficient: a chain can be correct piece by
piece and wrong end to end, and only this test catches that. In the project this template came
from, exactly this gap existed for months — the root-finding chain had been checked once, by
hand, outside the repository — and closing it permanently was a deliberate piece of work.

A skip is printed loudly and never counts as a pass.
