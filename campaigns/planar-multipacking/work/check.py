"""Independent planar subcubic Independent Set and planar Multipacking oracles."""

import argparse
import json
import random
import subprocess
import sys
from itertools import product
from pathlib import Path

import networkx as nx
import z3


def graph_of(instance):
    graph = nx.Graph()
    graph.add_nodes_from(range(instance["vertices"]))
    graph.add_edges_from(instance["edges"])
    return graph


def legal_graph(instance):
    if not isinstance(instance,dict):
        return False
    n,edges,t = (instance.get(key) for key in ("vertices","edges","threshold"))
    if (type(n) is not int or n < 0 or type(t) is not int or t < 0
            or not isinstance(edges,list)):
        return False
    seen = set()
    for edge in edges:
        if (not isinstance(edge,list) or len(edge) != 2
                or any(type(v) is not int or not 0 <= v < n for v in edge)
                or edge[0] == edge[1]):
            return False
        key = tuple(sorted(edge))
        if key in seen:
            return False
        seen.add(key)
    return nx.is_planar(graph_of(instance))


def legal_source(source):
    return (legal_graph(source)
            and all(degree <= 3 for _,degree in graph_of(source).degree()))


def legal_target(target):
    return legal_graph(target)


def direct_set(instance,vertices):
    n = instance["vertices"]
    return (isinstance(vertices,list) and len(vertices) >= instance["threshold"]
            and all(type(v) is int and 0 <= v < n for v in vertices)
            and len(set(vertices)) == len(vertices))


def direct_independent(source,vertices):
    return (legal_source(source) and direct_set(source,vertices)
            and all(not (u in vertices and v in vertices) for u,v in source["edges"]))


def direct_multipacking(target,vertices):
    if not legal_target(target) or not direct_set(target,vertices):
        return False
    graph = graph_of(target)
    chosen = set(vertices)
    n = target["vertices"]
    for center in range(n):
        distances = nx.single_source_shortest_path_length(graph,center)
        for radius in range(1,n+1):
            if sum(v in chosen and distance <= radius for v,distance in distances.items()) > radius:
                return False
    return True


def source_solutions(source,limit=3):
    if not legal_source(source):
        raise ValueError("Illegal planar subcubic Independent Set instance")
    n = source["vertices"]
    selected = [z3.Bool(f"chosen_{v}") for v in range(n)]
    solver = z3.Solver()
    solver.add(z3.Sum(*[z3.If(value,1,0) for value in selected]) >= source["threshold"])
    for u,v in source["edges"]:
        solver.add(z3.Or(z3.Not(selected[u]),z3.Not(selected[v])))
    outputs = []
    while len(outputs) < limit:
        result = solver.check()
        if result == z3.unsat:
            break
        if result != z3.sat:
            raise RuntimeError(f"Inconclusive source solver: {result}")
        model = solver.model()
        values = [z3.is_true(model.eval(x,model_completion=True)) for x in selected]
        vertices = [v for v,value in enumerate(values) if value]
        if not direct_independent(source,vertices):
            raise AssertionError("Z3 independent set failed direct validation")
        outputs.append({"set":vertices})
        solver.add(z3.Or(*[x != value for x,value in zip(selected,values)]))
    return outputs or [{"status":"NO-SOLUTION"}]


def solve_source(source):
    return source_solutions(source,1)[0]


def valid_source(source,output):
    if not legal_source(source) or not isinstance(output,dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_source(source) == output
    return set(output) == {"set"} and direct_independent(source,output["set"])


def target_solutions(target,limit=3):
    if not legal_target(target):
        raise ValueError("Illegal planar Multipacking instance")
    n = target["vertices"]
    graph = graph_of(target)
    selected = [z3.Bool(f"packed_{v}") for v in range(n)]
    solver = z3.Solver()
    solver.add(z3.Sum(*[z3.If(value,1,0) for value in selected]) >= target["threshold"])
    for center in range(n):
        distances = nx.single_source_shortest_path_length(graph,center)
        for radius in range(1,n+1):
            ball = [z3.If(selected[v],1,0) for v,distance in distances.items()
                    if distance <= radius]
            solver.add(z3.Sum(*ball) <= radius)
    outputs = []
    while len(outputs) < limit:
        result = solver.check()
        if result == z3.unsat:
            break
        if result != z3.sat:
            raise RuntimeError(f"Inconclusive target solver: {result}")
        model = solver.model()
        values = [z3.is_true(model.eval(x,model_completion=True)) for x in selected]
        vertices = [v for v,value in enumerate(values) if value]
        if not direct_multipacking(target,vertices):
            raise AssertionError("Z3 multipacking failed direct validation")
        outputs.append({"set":vertices})
        solver.add(z3.Or(*[x != value for x,value in zip(selected,values)]))
    return outputs or [{"status":"NO-SOLUTION"}]


def solve_target(target):
    return target_solutions(target,1)[0]


def valid_target(target,output):
    if not legal_target(target) or not isinstance(output,dict):
        return False
    if output == {"status":"NO-SOLUTION"}:
        return solve_target(target) == output
    return set(output) == {"set"} and direct_multipacking(target,output["set"])


def exhaustive_source(source):
    n = source["vertices"]
    for bits in product((False,True),repeat=n):
        vertices = [v for v,value in enumerate(bits) if value]
        if direct_independent(source,vertices):
            return {"set":vertices}
    return {"status":"NO-SOLUTION"}


def exhaustive_target(target):
    n = target["vertices"]
    for bits in product((False,True),repeat=n):
        vertices = [v for v,value in enumerate(bits) if value]
        if direct_multipacking(target,vertices):
            return {"set":vertices}
    return {"status":"NO-SOLUTION"}


def self_test():
    from generate_cases import EDGE_CASES,random_source
    from test_oracle import test_hand_cases

    root = Path(__file__).resolve().parents[3]
    path = Path(__file__).with_name("cases.json")
    subprocess.run([sys.executable,str(root/"research/validate_preparation.py"),str(path)],check=True,cwd=root)
    cases = json.loads(path.read_text())
    for source,expected in EDGE_CASES:
        assert ("set" in solve_source(source)) == expected
    for case in cases:
        source = case["source"]
        if case["kind"] == "random":
            assert random_source(case["seed"]) == source
        current = solve_source(source)
        assert ("set" in current) == ("set" in case["expected"]) == ("set" in exhaustive_source(source))
        assert valid_source(source,current) and valid_source(source,case["expected"])
    test_hand_cases()
    checked, seen_targets = 0, set()
    for seed in range(100):
        rng = random.Random(seed)
        n = rng.randrange(7)
        edges = [[u,v] for u in range(n) for v in range(u+1,n)
                 if rng.randrange(3) == 0]
        for t in {1,(n+1)//2}:
            target = {"vertices":n,"edges":edges,"threshold":t}
            key = json.dumps(target,sort_keys=True)
            if key not in seen_targets and legal_target(target):
                seen_targets.add(key)
                assert ("set" in solve_target(target)) == ("set" in exhaustive_target(target))
                checked += 1
    print(f"Self-test passed: {len(cases)} independently labelled source cases and {checked} exhaustive planar target thresholds")


def candidate_check(path):
    self_test()
    cases = json.loads(Path(__file__).with_name("cases.json").read_text())
    recovered = 0
    for case in cases:
        source = case["source"]
        forward = subprocess.run([sys.executable,str(path)],input=json.dumps(source),text=True,capture_output=True,check=True)
        target = json.loads(forward.stdout)
        if not legal_target(target):
            raise AssertionError(f"Illegal planar target: {target}")
        for output in target_solutions(target):
            if not valid_target(target,output):
                raise AssertionError(f"Invalid target oracle output: {output}")
            payload = {"source":source,"target_solution":output}
            extraction = subprocess.run([sys.executable,str(path),"--extract"],input=json.dumps(payload),text=True,capture_output=True,check=True)
            recovered_output = json.loads(extraction.stdout)
            if not valid_source(source,recovered_output):
                raise AssertionError(f"Invalid recovery from {output}: {recovered_output}")
            recovered += 1
    print(f"Candidate check passed: {len(cases)} source cases, {recovered} target outputs")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--self-test",action="store_true")
    group.add_argument("--candidate",type=Path)
    args = parser.parse_args()
    if args.self_test:
        self_test()
    else:
        candidate_check(args.candidate)
