import os
import pickle


def get_img_loc(filename):
    url = os.getcwd()
    dir = "assets"
    url = os.path.join(url, dir)
    return os.path.join(url, filename)


def load_pickle(name):
    with open(name + ".pkl", "rb") as f:
        return pickle.load(f)