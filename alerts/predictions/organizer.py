"""Organize alerts."""

import pandas as pd


if __name__ == "__main__":
    f = open("samples/sample1.csv")
    data = pd.read_csv(f)
    for eid in data["EventID"]:
        print(eid)
    print("DONE")
    if __debug__:
        print("THIS IS DEBUG")
    x = True
    assert(x)
    assert(not x)
    print(x)
