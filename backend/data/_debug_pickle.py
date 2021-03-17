import pickle
import json
from os import path


def dump_pickle_repr():
    """
    Local testing function for checking the state of the pickle
    """
    with open(path.join(path.dirname(__file__), "store.pickle"), "rb") as f:
        print(json.dumps(pickle.load(f)))


if __name__ == "__main__":
    dump_pickle_repr()
