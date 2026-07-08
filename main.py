# Git repo (unit tests live under tests/, run with: pytest --cov=kfc): TODO - add your repo URL here
import sys

from kfc.app import KongFuChessApp


def main() -> None:
    app = KongFuChessApp()
    app.run(sys.stdin, sys.stdout)


if __name__ == "__main__":
    main()
