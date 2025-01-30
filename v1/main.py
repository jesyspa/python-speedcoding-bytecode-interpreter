from lexer import make_rule, Lexer
from parser import parse
from vm import VM

# Syntax:
# instructions:
# - mov tgt src
# - math_op tgt src
# - jump cond tgt
# - input/output tgt
# register 0 is program counter
# targets:
# - literal
# - register
# - indirect register
# - memory
# register 1 is always used for conditions

@make_rule('INSTRUCTION', 'mov|input|output|add|mul|jump')
def instruction(match):
    return match.group()

def resolve_target_prefix(prefix):
    match prefix:
        case 'a':
            return 'ADDRESS'
        case 'i':
            return 'INDIRECT'
        case 'r':
            return 'REGISTER'
        case '':
            return 'LITERAL'
        case _:
            raise Exception(f"Unknown target prefix {prefix}")

@make_rule('TARGET', r'([a-z]?)(-?\d+)')
def target(match):
    return resolve_target_prefix(match.group(1)), int(match.group(2))

@make_rule('CONDITION', r'zero|pos|neg|nonzero')
def condition(match):
    return match.group().upper()

DEFAULT_EXAMPLE = 'examples/fibonacci'

def main():
    with open(DEFAULT_EXAMPLE, 'r') as f:
        program = f.read()
    lexer = Lexer([instruction, target, condition], program)
    program = parse(lexer)
    vm = VM(program)
    vm.run()

if __name__ == '__main__':
    main()