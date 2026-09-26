# Prepared input and output contract

The source and target use `{"vertices": n, "edges": [[u,v], ...],
"threshold": k}` with a simple undirected planar graph on `0..n-1` and
nonnegative integer `k`. The source additionally requires maximum degree
at most three. A source output is `{"set": [distinct_vertices]}` with at
least `k` vertices and no edge internal to the set, or
`{"status": "NO-SOLUTION"}` exactly when none exists.

A target output is `{"set": [distinct_vertices]}` with at least `k`
vertices such that for every center vertex and every integer radius from
one through `n`, its closed shortest-path ball contains at most that many
selected vertices. Unreachable vertices do not belong to a finite-radius
ball. `{"status": "NO-SOLUTION"}` is valid exactly when no such
multipacking exists. The empty graph has a valid empty set when `k=0`.

A candidate `algorithm.py` reads source JSON from stdin and writes legal
target JSON to stdout. With `--extract`, it reads
`{"source": source, "target_solution": output}` and writes a valid source
output. The commands share no memory, exit nonzero on errors, and send
diagnostics to stderr. They must be deterministic and polynomial time;
recovery must work for every valid target multipacking and negative answer.

`check.py --candidate PATH` independently solves constructed targets on
the fixed source corpus and directly validates recovered source outputs.
