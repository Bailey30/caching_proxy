import argparse
from dataclasses import dataclass


@dataclass
class Args:
    origin: int
    port: str
    clear_cache: bool


def get_args() -> Args:
    parser = argparse.ArgumentParser()

    parser.add_argument("-p", "--port", type=int, required=True)
    parser.add_argument("-o", "--origin", type=str, required=True)
    parser.add_argument("-cc", "--clear-cache", type=bool, default=False)

    args = parser.parse_args()
    print(args)

    return Args(origin=args.origin, port=args.port, clear_cache=args.clear_cache)
