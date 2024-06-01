class DataPath:
    def __init__(self, memory: [], input_data: []):
        self.address = 0
        self.registers = [0] * 18
        self.registers[-3] = -2
        self.registers[-4] = 1  # 0 - reg -> out, 1 - memory -> reg -> out
        self.registers[-5] = -1
        self.buffer = [input_data, []]
        self.memory = memory

    def set_right_register_address(self, address):
        self.registers[-1] = address

    def set_left_register_address(self, address):
        self.registers[-2] = address

    def zero(self):
        return self.registers[-5] == 0

    def je_condition(self):
        return self.registers[-3] == 0

    def jl_condition(self):
        return self.registers[-3] == -1

    def jb_condition(self):
        return self.registers[-3] == 1

    def set_address(self, addr):
        self.address = addr

    def inc_address(self):
        self.address += 1

    def dec_address(self):
        self.address -= 1

    def write_value_to_memory(self, sel, r_number, operation, port):
        if sel == -1:
            self.memory[self.address] = ord(self.buffer[port].pop())
        elif sel == 0:
            self.memory[self.address] = self.perform_alu_operation(operation)
        elif sel == 1:
            self.memory[self.address] = self.registers[r_number]
        elif sel == 2:
            self.memory[self.address] = self.registers[self.registers[-2]]
        elif sel == 3:
            self.memory[self.address] = self.registers[self.registers[-1]]

    def write_value_to_register(self, sel, r_number, operation, port):
        if sel == -1:
            self.registers[-5] = ord(self.buffer[port].pop())
        elif sel == 0:
            if r_number is None:
                self.registers[self.registers[-2]] = self.perform_alu_operation(operation)
            else:
                self.registers[r_number] = self.perform_alu_operation(operation)
        elif sel == 1:
            self.registers[r_number] = self.memory[self.address]
        elif sel == 2:
            self.registers[self.registers[-2]] = self.memory[self.address]
        elif sel == 3:
            self.registers[self.registers[-1]] = self.memory[self.address]

    def out_register(self, translation_status, port):
        out = self.registers[-5]
        if translation_status:
            self.buffer[port].append(str(chr(out)))
        else:
            self.buffer[port].append(str(out))

    def perform_alu_operation(self, operation):
        value_1 = self.registers[self.registers[-2]]
        value_2 = self.registers[self.registers[-1]]
        new_value = 0
        if operation in list(actions_for_alu.keys()):
            new_value = actions_for_alu[operation](value_1, value_2)
        else:
            print("Now it doesn't work")
        return new_value


actions_for_alu = {
    "+": lambda x, y: x + y,
    "-": lambda x, y: x - y,
    "*": lambda x, y: x * y,
    "/": lambda x, y: round(x / y, 1),
    "%": lambda x, y: x % y,
    "inc": lambda x, y: x + 1,
    "dec": lambda x, y: x - 1,
    "<": lambda x, y: -1 if x < y else 0 if x == y else 1,
    "==": lambda x, y: -1 if x < y else 0 if x == y else 1,
    ">": lambda x, y: -1 if x < y else 0 if x == y else 1,
    "1": lambda x, y: 1,
    "0": lambda x, y: 0,
}
