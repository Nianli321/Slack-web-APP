from os import path, remove
import pickle

# Relative to the server directory
SERVER_DIR = path.dirname(__file__)
DATA_STORE_PATH = path.join(SERVER_DIR, "data", "store.pickle")


def load_data_store(store_file_path=DATA_STORE_PATH):
    """
    Loads the data from the data store
    If no store, just return empty dictionary
    """
    try:
        with open(store_file_path, "rb") as store_file:
            return pickle.load(store_file)
    except FileNotFoundError:
        return {}


def dump_data_store(data, store_file_path=DATA_STORE_PATH):
    """
    Dumps the data to the data store
    If no store, create a new one
    """
    with open(store_file_path, "wb") as store_file:
        return pickle.dump(data, store_file)


def clear_data_store(store_file_path=DATA_STORE_PATH):
    """
    Removes the data store
    """
    try:
        remove(store_file_path)
    except FileNotFoundError:
        return
