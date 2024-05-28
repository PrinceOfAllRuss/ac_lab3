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
            return self.acc
        else:
            self.buffer[port].append(str(self.acc))
            return self.acc
    def data_address(self, addr, inc, dec):
        if inc:
            return addr + 1
        elif dec:
            return addr - 1
        else:
            addr
    def perform_alu_operation(self, operation):
        value_1 = self.acc
        value_2 = self.memory[self.address]
        if operation == "+":
            return value_1 + value_2
        elif operation == "-":
            return value_1 - value_2
        elif operation == "*":
            return value_1 * value_2
        elif operation == "/":
            return value_1 / value_2
        elif operation == "%":
            return value_1 % value_2
        elif operation == "<" or operation == "==" or operation == ">":
            if value_1 < value_2:
                return -1
            elif value_1 == value_2:
                return 0
            elif value_1 > value_2:
                return 1
        elif operation == "inc":
            return value_1 + 1
        elif operation == "dec":
            return value_1 - 1
        else:
            print("Now it doesn't work")
            return 0