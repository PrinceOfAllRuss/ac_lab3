opcode = ["mov", "inc", "dec", "add", "sub", "mul", "div", "jmp", "jz", "jnz", "cmp", "in", "out", "halt"]

class Operation():
    def __init__(self, name, index, args):
        self.name = name
        self.index = index
        self.args = args