# Preparation evidence

Prepared on 2026-09-26 before constructing a candidate. The fixed corpus
contains 117 distinct legal planar subcubic Independent Set instances:
17 hand-labelled edge cases and 100 seeded random cases, with 87 YES and
30 NO decisions and zero to eight vertices. The generator and seeds are in
`generate_cases.py`; checked outputs are in `cases.json`. NetworkX 3.6.1
checks planarity and vertex degrees. Z3 4.16.0 encodes selection size and
edge exclusion. Returned independent sets are checked directly, and Z3
UNSAT is conclusive; unknown is an error. Exhaustive subset enumeration
agreed with the source oracle on all 117 cases.

For the target, NetworkX computes exact unweighted shortest-path lengths.
Z3 constrains the selected count in every closed ball of radius `1..n`.
The direct validator recomputes each ball and count independently of the
Z3 constraints. This covers disconnected graphs, where unreachable vertices
are absent from the ball. Exhaustive subset enumeration agreed with Z3 on
89 distinct planar graph/threshold combinations with up to six vertices.
Hand fixtures distinguish Independent Set from full Multipacking on a
three-vertex path, exercise a radius-two ball on a four-vertex path, and
reject nonplanar K5 and malformed graphs. The ball semantics follow the
[primary paper](https://arxiv.org/html/2602.07982v1); planarity is checked
by [NetworkX's documented algorithm](https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.planarity.is_planar.html).

Reproduce from the repository root:

```sh
uv sync --locked
uv run --locked python campaigns/planar-multipacking/work/check.py --self-test
```

The self-test starts with the corpus gate, regenerates seeded graphs,
rechecks source labels and witnesses, and compares target decisions to
exhaustive enumeration. The candidate runner uses separate forward and
recovery subprocesses and up to three target multipackings per source.
An incorrect injected candidate was rejected after target solving and
source validation. No actual reduction candidate exists; finite checks
do not establish hardness or a general reduction.
