from data_path import DataPath
class ControlUnit:
    def __init__(self, memory: list[dict], data_path):
        self.memory = memory
        self.tick = 0
        self.program_counter = 0
        self.data_path = DataPath(memory)

    def process(self):
        i = 0
        address = i
        while "operation" in list(self.memory[i].keys):
            next = self.data_path.start_stub(self.memory[i])
            new_address = self.mux_for_address(next)
            if address + 1 == new_address:
                i += 1
            else:
                while True:
                    next = self.data_path.start_stub(self.memory[new_address])
                    new_address = self.mux_for_address(next)
                    if address + 1 == new_address:
                        i += 1
                        break

    def mux_for_address(self, next, address):
        self.program_counter += 1
        if next == 0:
            return address + 1
        else:
            return address + next