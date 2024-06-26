import logging

from data_path import DataPath
from isa import Operation, opcode, opcode_keys


class ControlUnit:
    def __init__(self, memory: [], input_data):
        self.memory = memory
        self.address = 0
        self.tick_counter = 0
        self.program_counter = 0
        self.data_path = DataPath(memory, input_data)
        self.program_end_condition = False

    def tick(self):
        self.tick_counter += 1

    def select_address(self, next_addr):
        if next_addr is None:
            self.address += 1
        else:
            self.address = next_addr

    def start(self, limit):
        self.program_counter = 0
        try:
            while not self.program_end_condition and self.program_counter < limit:
                operation: Operation = self.memory[self.address]
                logging.debug(
                    f"PC: {self.program_counter} TICK: {self.tick_counter} P_ADDR: {self.address} "
                    f"MEM_ADDR: {self.data_path.address} REGS: {self.data_path.registers} "
                    f"COMMAND: {operation.name} {operation.args}"
                )
                if operation.name in opcode_keys:
                    callable_operation: Operation = opcode[operation.name]
                    callable_operation.name = operation.name
                    callable_operation.args = operation.args
                    callable_operation.execute(self)
                self.tick()
                self.program_counter += 1
        except EOFError:
            logging.warning("Input buffer is empty!")
        return self.data_path.buffer[1]
