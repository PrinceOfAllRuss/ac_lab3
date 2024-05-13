class DataPath:
    def __init__(self, memory):
        self.memory = memory
        self.acc = 0
        self.buff = 0
    def execute_command(self, addr, memory):
        addr = self.data_address(addr, False, False)

        el = memory[addr]

    def data_address(self, addr, inc, dec):
        if inc:
            return addr + 1
        elif dec:
            return addr - 1
        else:
            addr