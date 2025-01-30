from lexer import lex
from parser import parse
from vm import VM

DEFAULT_EXAMPLE = 'examples/fibonacci'

def repl():
    vm = None
    while True:
        line = input('> ').split()
        if len(line) == 0:
            continue
        match line[0]:
            case "quit":
                return
            case "load":
                path = line[1] if len(line) > 1 else 'examples/fibonacci'
                with open(path, "r") as file:
                    source = file.read()
                lexed = lex(source)
                vm = VM(parse(lexed))
                vm.print()
            case "run":
                vm.run()
            case "step":
                vm.step()
                vm.print()
            case "show":
                n = int(line[1]) if len(line) > 1 else None
                vm.print(n)
            case _:
                print(f"Unknown command: {line[0]}")

if __name__ == '__main__':
    repl()
