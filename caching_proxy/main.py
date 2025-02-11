from .cache import Cache
from .server import Server
from .args import get_args


def main():
    args = get_args()

    cache = Cache(10)

    Server(port=args.port, origin=args.origin, cache=cache).start()


if __name__ == "__main__":
    main()
