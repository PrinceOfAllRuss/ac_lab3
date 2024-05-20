class DataPath:
    def __init__(self, memory):
        self.memory = memory
        self.address = 0
        self.acc = 0
        self.port_latch = -1
        self.line_break_latch = -1
        self.alu = "+"

    def set_alu(self, operation):
        self.alu = operation
    def set_address(self, addr):
        self.address = addr
    def set_line_break(self, line_break):
        self.line_break_latch = line_break
    def inc_address(self):
        self.address += 1
    def dec_address(self):
        self.address -= 1
    def read_value(self):
        self.acc = self.memory[self.address]
        return self.acc
    def write_value(self, value):
        self.memory[self.address] = value
    def out_acc(self, translation_status):
        if self.port_latch == 0:
            self.mux_for_output(translation_status)
    def data_address(self, addr, inc, dec):
        if inc:
            return addr + 1
        elif dec:
            return addr - 1
        else:
            addr
    def perform_alu_operation(self):
        value_1 = self.memory[self.address]
        value_2 = self.acc
        if self.alu == "+":
            self.acc = value_1 + value_2
        else:
            print("Now it doesn't work")
    def write_value_to_memory_from_acc(self):
        self.memory[self.address] = self.acc
    def set_port_latch(self, port):
        self.port_latch = port
    def mux_for_output(self, translation_status):
        if translation_status:
            self.mux_for_str_output()
        else:
            print(self.acc)
    def mux_for_str_output(self):
        if self.line_break_latch == -1:
            print(chr(self.acc), end="")
        else:
            print(chr(self.acc))