from data_path import DataPath
from isa import Operation, opcode, opcode_keys

class ControlUnit:
    def __init__(self, memory: []):
        self.memory = memory
        self.address = 0
        self.tick_counter = 0
        self.program_counter = 0
        self.data_path = DataPath(memory)
        self.command_limit = 10
        self.program_end_condition = False

    def tick(self):
        self.tick_counter += 1

    def mux_for_address(self, next):
        self.program_counter += 1
        if next is None:
            self.address += 1
        else:
            self.address = next
    def start(self):
        self.program_counter = 1
        while not self.program_end_condition:
            if self.program_counter >= self.command_limit:
                print("End of program by command limit")
                break
            operation: Operation = self.memory[self.address]
            if operation.name in opcode_keys:
                callable_operation: Operation = opcode[operation.name]
                callable_operation.name = operation.name
                callable_operation.args = operation.args
                callable_operation.perform(self)

            if operation.name in ["jump", "jnz", "jz"]:
                new_address = operation.get_value(0)
                self.mux_for_address(new_address)
                self.tick()
            else:
                self.mux_for_address(None)
                self.tick()

            self.program_counter += 1
