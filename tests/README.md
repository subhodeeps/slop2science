# tests

    julia/runtests.jl      entry point for the Julia tests
    python/                pytest tests

    make test              runs each language that is present; skips an absent language, loudly

## The test that matters most

Each topic needs at least one **known-answer test of the full chain**. Use a problem with an
exact closed-form solution. Run it through the same path that the real solver uses: assembly,
solve, refinement, acceptance. Do this in each precision tier that the project uses.

Unit tests of each piece are necessary. They are not sufficient. A chain can be correct piece
by piece and wrong from end to end. Only this test finds that fault. In the project that this
template came from, this gap existed for months. Someone checked the root-finding chain once,
by hand, outside the repository. Closing the gap permanently was a deliberate piece of work.

The test run prints a skip loudly. A skip never counts as a pass.
