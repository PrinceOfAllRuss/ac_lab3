class Operation():
    def __init__(self, name = "", args = []):
        self.name = name
        self.args = args
    def get_address(self, index):
        address = self.args[index]
        address_index = int(address[1:])
        return address_index
    def get_value(self, index):
        return self.args[index]
    def perform(self, control_unit):
        return
class Add(Operation):
    def perform(self, control_unit):
        control_unit.data_path.set_alu("+")
        control_unit.tick()

        first_address = self.get_address(0)
        control_unit.data_path.set_address(first_address)
        control_unit.tick()

        control_unit.data_path.read_value()
        control_unit.tick()

        for i in range(1, len(self.args) - 1):
            adds = self.get_address(i)
            control_unit.data_path.set_address(adds)
            control_unit.tick()

            control_unit.data_path.perform_alu_operation()
            control_unit.tick()

        last_address = self.get_value(-1)
        control_unit.data_path.set_address(last_address)
        control_unit.tick()

        control_unit.data_path.write_value_to_memory_from_acc()
        control_unit.tick()
class Halt(Operation):
    def perform(self, control_unit):
        print("End of program by HALT")
        control_unit.program_end_condition = True
class Out(Operation):
    def perform(self, control_unit):
        port = self.get_value(0)
        control_unit.data_path.set_port_latch(port)
        control_unit.tick()

        control_unit.data_path.read_value()
        control_unit.tick()

opcode = {"add": Add(), "out": Out(), "halt": Halt()}
opcode_keys = ["mov", "inc", "dec", "add", "sub", "mul", "div", "jmp", "jz", "jnz", "cmp", "in", "out", "halt"]