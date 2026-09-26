"""Fix seeded planar subcubic Independent Set cases before construction."""

import json
import random
from pathlib import Path


def graph(n,edges,t):
    return {"vertices":n,"edges":edges,"threshold":t}


EDGE_CASES = [
    (graph(0,[],0),True), (graph(0,[],1),False),
    (graph(1,[],0),True), (graph(1,[],1),True), (graph(1,[],2),False),
    (graph(2,[[0,1]],2),False), (graph(2,[],2),True),
    (graph(3,[[0,1],[1,2]],2),True),
    (graph(3,[[0,1],[1,2],[0,2]],2),False),
    (graph(4,[[0,1],[1,2],[2,3],[0,3]],2),True),
    (graph(4,[[0,1],[1,2],[2,3],[0,3]],3),False),
    (graph(4,[[0,1],[0,2],[0,3]],3),True),
    (graph(4,[[0,1],[0,2],[0,3]],4),False),
    (graph(4,[[u,v] for u in range(4) for v in range(u+1,4)],2),False),
    (graph(4,[[u,v] for u in range(4) for v in range(u+1,4)],1),True),
    (graph(5,[[0,1],[1,2],[2,3],[3,4]],3),True),
    (graph(5,[[0,1],[1,2],[2,3],[3,4],[0,4]],3),False),
]


def random_source(seed):
    rng = random.Random(seed)
    n = rng.randint(4,8)
    degrees = [0]*n
    edges = []
    for u in range(n):
        for v in range(u+1,min(n,u+3)):
            if degrees[u] < 3 and degrees[v] < 3 and rng.random() < 0.65:
                edges.append([u,v])
                degrees[u] += 1
                degrees[v] += 1
    if seed % 2 == 0:
        chosen = []
        for v in rng.sample(range(n),n):
            if not any({u,v} == set(edge) for u in chosen for edge in edges):
                chosen.append(v)
        threshold = len(chosen)
    else:
        threshold = n//2+1
    return graph(n,edges,threshold)


def build_cases():
    from check import solve_source
    cases, seen = [], set()

    def add(source,kind,seed=None,hand_answer=None):
        key = json.dumps(source,sort_keys=True,separators=(",", ":"))
        if key in seen:
            return False
        seen.add(key)
        answer = solve_source(source)
        if hand_answer is not None and ("set" in answer) != hand_answer:
            raise AssertionError(f"Hand label disagrees with oracle: {source}")
        case = {"source":source,"kind":kind,"expected":answer}
        if seed is not None:
            case["seed"] = seed
        cases.append(case)
        return True

    for source,expected in EDGE_CASES:
        add(source,"edge",hand_answer=expected)
    seed = 0
    while sum(case["kind"] == "random" for case in cases) < 100:
        add(random_source(seed),"random",seed=seed)
        seed += 1
    return cases


if __name__ == "__main__":
    path = Path(__file__).with_name("cases.json")
    cases = build_cases()
    path.write_text(json.dumps(cases,indent=2)+"\n")
    print(f"Wrote {len(cases)} cases to {path}")
