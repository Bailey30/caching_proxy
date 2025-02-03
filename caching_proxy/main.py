from .cache import Cache
from .server import Server
from .args import get_args


def main():
    import sys

    print(sys.executable)
    args = get_args()

    print(args)

    cache = Cache(10)

    server = Server(port=args.port, origin=args.origin, cache=cache)

    cache.print_map()


if __name__ == "__main__":
    main()
