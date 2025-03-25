# Goes in __init__.py
from .add import add

__all__ = ['add']


def main() -> None:
    print("Hello from packaging-workshop-bif!")
