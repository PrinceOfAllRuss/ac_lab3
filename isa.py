# from control_unit import ControlUnit
class Operation():
    def __init__(self, name = "", args = []):
        self.name = name
        self.args = args
    def get_address(self, index):
        address = self.args[index]
        address_index = int(address[1:])
        return address_index
    # def perform(self, control_unit: ControlUnit):
    #     return
    def perform(self, control_unit):
        return
class Mov(Operation):
    def perform(self, control_unit):
        if len(self.args) == 1:
            control_unit.data_path.set_address(self.get_address(0))
            control_unit.tick()
        else:
            """
            Тут должна быть обработка перемещения элемента из одной ячейкм памяти в другую
            """
            # control_unit.data_path.set_address(self)
            # control_unit.tick()
        control_unit.mux_for_address(None)
class Jmp(Operation):
    def perform(self, control_unit):
        next_operation_address = self.get_address(0)
        control_unit.mux_for_address(next_operation_address)
class Jz(Operation):
    def perform(self, control_unit):
        if control_unit.conditional_jump_buffer == 0:
            next_operation_address = self.get_address(0)
            control_unit.mux_for_address(next_operation_address)
            control_unit.conditional_jump_buffer = -1
            control_unit.tick()
        else:
            control_unit.mux_for_address(None)

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

        last_address = self.args[-1]
        control_unit.data_path.set_address(last_address)
        control_unit.tick()

        control_unit.data_path.write_value_to_memory_from_acc()
        control_unit.tick()

        control_unit.mux_for_address(None)
class In(Operation):
    def perform(self, control_unit):
        adds = self.args[-1]
        control_unit.data_path.set_address(adds)
        control_unit.tick()

        value = input()
        for i in value:
            control_unit.data_path.write_value(ord(i))
            control_unit.tick()
            control_unit.data_path.inc_address()
            control_unit.tick()

        control_unit.data_path.write_value(ord("\n"))
        control_unit.tick()
        control_unit.data_path.inc_address()
        control_unit.tick()
        control_unit.data_path.write_value(ord("\0"))
        control_unit.tick()
        control_unit.data_path.set_address(adds)
        control_unit.tick()

        control_unit.mux_for_address(None)
class Out(Operation):
    def perform(self, control_unit):
        port = self.args[0]
        type = self.args[-1]

        # if len(self.args) == 3:
        #     addr = self.args[1]
        #     control_unit.data_path.set_address(addr)
        #     control_unit.tick()

        if type == "numb":
            control_unit.data_path.set_port_latch(port)
            control_unit.tick()

            control_unit.data_path.read_value()
            control_unit.tick()

            control_unit.data_path.out_acc(False)
            control_unit.tick()
        elif type == "str":
            control_unit.data_path.set_port_latch(port)
            control_unit.tick()

            control_unit.conditional_jump_buffer = control_unit.data_path.read_value()
            control_unit.tick()

            if control_unit.conditional_jump_buffer != 0:
                control_unit.data_path.out_acc(True)
                control_unit.tick()

                control_unit.data_path.inc_address()
                control_unit.tick()

        control_unit.mux_for_address(None)
class Halt(Operation):
    def perform(self, control_unit):
        print("End of program by HALT")
        control_unit.program_end_condition = True

opcode = {"mov": Mov(), "add": Add(), "jmp": Jmp(), "jz": Jz(), "in": In(), "out": Out(), "halt": Halt()}
opcode_keys = ["mov", "inc", "dec", "add", "sub", "mul", "div", "jmp", "jz", "jnz", "cmp", "in", "out", "halt"]