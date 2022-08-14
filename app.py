from concurrent.futures import ThreadPoolExecutor

from cpp_work import cpp_work

from python_work import python_work
from util import execute


def main() -> int:
    print("Doing python work using threads!")
    execute(ThreadPoolExecutor, work=python_work)

    print("Doing cpp work using threads!")
    execute(ThreadPoolExecutor, work=cpp_work)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
