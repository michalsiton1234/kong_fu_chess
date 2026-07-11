# Git repo (unit tests live under tests/, run with: pytest --cov=kungfu_chess): TODO - add your repo URL here
import sys

from kungfu_chess.app import KungFuChessApp


def main() -> None:
    KungFuChessApp().run(sys.stdin, sys.stdout)


if __name__ == "__main__":
    main()
