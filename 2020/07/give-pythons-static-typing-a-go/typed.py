def ultimate_answer() -> str:
    return "42"

def do_something(n: int):
    return n - 11

def main() -> None:
    u = do_something(ultimate_answer())

main()
