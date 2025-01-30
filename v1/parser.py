def parse(lexer):
    instructions = []
    while lexer:
        op = lexer.next_as('INSTRUCTION')
        match op:
            case 'jump':
                condition = lexer.next_as('CONDITION')
                target = lexer.next_as('TARGET')
                instructions.append((op, condition, target))
            case 'input' | 'output':
                target = lexer.next_as('TARGET')
                instructions.append((op, target))
            case 'mov' | 'add' | 'mul':
                target = lexer.next_as('TARGET')
                source = lexer.next_as('TARGET')
                instructions.append((op, target, source))
            case _:
                raise Exception(f'Invalid instruction {op}')
    return instructions


