from data_path import DataPath
from isa import Operation, opcode, opcode_keys

class ControlUnit:
    def __init__(self, memory: []):
        self.memory = memory
        self.address = 0
        self.tick_counter = 0
        self.program_counter = 0
        self.data_path = DataPath(memory)
        # self.command_limit = 100
        self.program_end_condition = False
        self.conditional_jump_buffer = -1

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
            operation: Operation = self.memory[self.address]
            if operation.name in opcode_keys:
                callable_operation: Operation = opcode[operation.name]
                callable_operation.name = operation.name
                callable_operation.args = operation.args
                callable_operation.perform(self)
            self.tick()
            self.program_counter += 1
