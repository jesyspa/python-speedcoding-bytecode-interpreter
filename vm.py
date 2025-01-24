MEMORY_SIZE = 1024
NUM_REGISTERS = 8

class TargetListAtIndex:
    def __init__(self, xs, ix):
        self.xs = xs
        self.ix = ix

    def get(self):
        return self.xs[self.ix]

    def update(self, value):
        self.xs[self.ix] = value

class TargetConstant:
    def __init__(self, c):
        self.c = c

    def get(self):
        return self.c

    def update(self, value):
        raise Exception("Cannot store to constant")

class VM:
    def __init__(self, program):
        self.program = program
        self.memory = [0] * MEMORY_SIZE
        self.registers = [0] * NUM_REGISTERS
        self.instruction_pointer = 0
        self.accumulator = 0

    def print(self, mem_start=None):
        print('REGS:', ' '.join(map(str, self.registers)))
        print('IP:', self.instruction_pointer)
        print('ACC:', self.accumulator)

        if mem_start is not None:
            print('MEM:', ' '.join(map(str, self.memory[mem_start:mem_start + 32])))

    def run(self):
        while self.step():
            pass

    def step(self):
        if self.instruction_pointer >= len(self.program):
            return False
        op, target, n = self.program[self.instruction_pointer]
        if op != 'jump':
            target = self.resolve_target(target, n)
        match op:
            case 'read':
                value = int(input('! '))
                target.update(value)
            case 'print':
                print(target.get())
            case 'load':
                self.accumulator = target.get()
            case 'store':
                target.update(self.accumulator)
            case 'add':
                self.accumulator += target.get()
            case 'mul':
                self.accumulator *= target.get()
            case 'jump':
                if self.check_condition(target):
                    self.instruction_pointer = n - 1
        self.instruction_pointer += 1
        return True

    def resolve_target(self, target, n):
        match target:
            case 'reg':
                return TargetListAtIndex(self.registers, n)
            case 'mem':
                return TargetListAtIndex(self.memory, n)
            case 'const':
                return TargetConstant(n)
            case 'indmem':
                return TargetListAtIndex(self.memory, self.registers[n])
            case _:
                raise Exception(f"Unknown target {target}")

    def check_condition(self, condition):
        match condition:
            case 'pos':
                return self.accumulator > 0
            case 'zero':
                return self.accumulator == 0
            case 'neg':
                return self.accumulator < 0
            case _:
                raise Exception(f"Unknown condition {condition}")

