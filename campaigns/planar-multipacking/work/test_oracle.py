from check import legal_source, solve_source, valid_source, legal_target, solve_target, valid_target


def test_hand_cases():
    path3 = {"vertices":3,"edges":[[0,1],[1,2]],"threshold":2}
    assert valid_source(path3,{"set":[0,2]})
    assert not valid_source(path3,{"set":[0,1]})
    assert solve_target(path3) == {"status":"NO-SOLUTION"}
    path4 = {"vertices":4,"edges":[[0,1],[1,2],[2,3]],"threshold":2}
    assert valid_target(path4,{"set":[0,3]})
    isolated = {"vertices":2,"edges":[],"threshold":2}
    assert valid_target(isolated,{"set":[0,1]})
    k5 = {"vertices":5,"edges":[[u,v] for u in range(5) for v in range(u+1,5)],"threshold":0}
    assert not legal_target(k5)
    assert not legal_source({"vertices":4,"edges":[[0,1],[0,2],[0,3],[0,3]],"threshold":1})


if __name__ == "__main__":
    test_hand_cases()
