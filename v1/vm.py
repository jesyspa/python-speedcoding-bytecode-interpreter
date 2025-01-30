NUM_REGISTERS = 8
MEMORY_SIZE = 1024

def resolve_condition(condition):
    match condition:
        case 'ZERO':
            return lambda x: x == 0
        case 'POS':
            return lambda x: x > 0
        case 'NEG':
            return lambda x: x < 0
        case 'NONZERO':
            return lambda x: x != 0
        case _:
            raise Exception(f"Unsupported condition {condition}")

class ListAccess:
    def __init__(self, list, index):
        self.list = list
        self.index = index

    def get(self):
        return self.list[self.index]

    def set(self, value):
        self.list[self.index] = value

class Constant:
    def __init__(self, value):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        raise Exception("Cannot assign to a constant")

class VM:
    def __init__(self, program):
        self.program = program
        self.registers = [0] * NUM_REGISTERS
        self.memory = [0] * MEMORY_SIZE

    def step(self):
        if self.registers[0] >= len(self.program):
            return False
        op = self.program[self.registers[0]]
        match op[0]:
            case 'mov':
                tgt = self.resolve_target(op[1])
                src = self.resolve_target(op[2])
                tgt.set(src.get())
            case 'output':
                src = self.resolve_target(op[1])
                print(src.get())
            case 'input':
                tgt = self.resolve_target(op[1])
                value = int(input('! '))
                tgt.set(value)
            case 'add':
                tgt = self.resolve_target(op[1])
                src = self.resolve_target(op[2])
                tgt.set(tgt.get() + src.get())
            case 'mul':
                tgt = self.resolve_target(op[1])
                src = self.resolve_target(op[2])
                tgt.set(tgt.get() * src.get())
            case 'jump':
                cond = resolve_condition(op[1])
                tgt = self.resolve_target(op[2])
                if cond(self.registers[1]):
                    self.registers[0] = tgt.get() - 1
        self.registers[0] += 1
        return True

    def run(self):
        while self.step():
            pass

    def resolve_target(self, target):
        match target[0]:
            case 'LITERAL':
                return Constant(target[1])
            case 'REGISTER':
                return ListAccess(self.registers, target[1])
            case 'ADDRESS':
                return ListAccess(self.memory, target[1])
            case 'INDIRECT':
                return ListAccess(self.memory, self.registers[target[1]])
            case _:
                raise Exception(f"Unsupported target {target}")

