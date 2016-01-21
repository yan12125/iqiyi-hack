import os.path

ROOT = os.path.dirname(os.path.abspath(__file__))


def full_path(p):
    return os.path.join(ROOT, p)
