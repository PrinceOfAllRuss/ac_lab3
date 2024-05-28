class DataPath:
    def __init__(self, memory: [], input_data: []):
        self.memory = memory
        self.address = 0
        self.acc = 0
        self.buffer = [input_data, []]

    def set_address(self, addr):
        self.address = addr
    def inc_address(self):
        self.address += 1
    def dec_address(self):
        self.address -= 1
    def write_value_to_memory(self, sel, operation, port):
        if sel == -1:
            self.memory[self.address] = ord(self.buffer[port].pop())
        elif sel == 0:
            self.memory[self.address] = self.perform_alu_operation(operation)
        elif sel == 1:
            self.memory[self.address] = self.acc
        return self.memory[self.address]
    def write_value_to_acc(self, sel, operation, port):
        if sel == -1:
            self.acc = ord(self.buffer[port].pop())
        elif sel == 0:
            self.acc = self.perform_alu_operation(operation)
        elif sel == 1:
            self.acc = self.memory[self.address]
        return self.acc
    def out_acc(self, translation_status, port):
        if translation_status:
            self.buffer[port].append(str(chr(self.acc)))
        else:
            self.buffer[port].append(str(self.acc))
        return self.acc
    def data_address(self, addr, inc, dec):
        new_addr = addr
        if inc:
            new_addr += 1
        elif dec:
            new_addr -= 1
        return new_addr
    def perform_alu_operation(self, operation):
        value_1 = self.acc
        value_2 = self.memory[self.address]
        new_value = 0
        if operation in list(actions_for_alu.keys()):
            new_value = actions_for_alu[operation](value_1, value_2)
        else:
            print("Now it doesn't work")
        return new_value
actions_for_alu = {"+": lambda x, y: x + y, "-": lambda x, y: x - y, "*": lambda x, y: x * y,
                   "/": lambda x, y: x / y, "%": lambda x, y: x % y, "inc": lambda x, y: x + 1,
                   "dec": lambda x, y: x - 1, "<": lambda x, y: -1 if x < y else 0 if x == y else 1,
                   "==": lambda x, y: -1 if x < y else 0 if x == y else 1,
                   ">": lambda x, y: -1 if x < y else 0 if x == y else 1}
