class Operation():
    def __init__(self, name = "", args = []):
        self.name = name
        self.args = args
    def perform(self, control_unit):
        return
class Mov(Operation):
    def perform(self, control_unit):
        if len(self.args) == 1:
            control_unit.data_path.set_address(self.args[0])
            control_unit.tick()
        else:
            """
            Тут должна быть обработка перемещения элемента из одной ячейкм памяти в другую
            """
            # control_unit.data_path.set_address(self)
            # control_unit.tick()
        control_unit.select_address(None)
class Jmp(Operation):
    def perform(self, control_unit):
        next_operation_address = self.args[0]
        control_unit.select_address(next_operation_address)
class Jz(Operation):
    def perform(self, control_unit):
        if control_unit.conditional_jump_buffer == 0:
            next_operation_address = self.args[0]
            control_unit.select_address(next_operation_address)
            control_unit.conditional_jump_buffer = -1
            control_unit.tick()
        else:
            control_unit.select_address(None)

class Add(Operation):
    def perform(self, control_unit):
        first_address = self.args[0]
        control_unit.data_path.set_address(first_address)
        control_unit.tick()

        control_unit.data_path.read_value()
        control_unit.tick()

        for i in range(1, len(self.args) - 1):
            adds = self.args[i]
            control_unit.data_path.set_address(adds)
            control_unit.tick()

            control_unit.data_path.write_value_to_acc(0, "+", None)
            control_unit.tick()

        last_address = self.args[-1]
        control_unit.data_path.set_address(last_address)
        control_unit.tick()

        control_unit.data_path.write_value_to_memory(1, "+", None)
        control_unit.tick()

        control_unit.select_address(None)
class In(Operation):
    def perform(self, control_unit):

        if len(self.args) == 2:
            addr = self.args[1]
            control_unit.data_path.set_address(addr)
            port = self.args[0]
            control_unit.out_condition = 1

            while control_unit.conditional_jump_buffer != 0:
                control_unit.conditional_jump_buffer = control_unit.data_path.write_value_to_memory(-1, None, port)
                control_unit.tick()
                control_unit.data_path.inc_address()
                control_unit.tick()
            control_unit.conditional_jump_buffer = -1
            control_unit.data_path.set_address(addr)
            control_unit.tick()
        else:
            port = self.args[0]
            control_unit.out_condition = 0
            control_unit.conditional_jump_buffer = control_unit.data_path.write_value_to_acc(-1, None, port)
            control_unit.tick()

        control_unit.select_address(None)
class Out(Operation):
    def perform(self, control_unit):
        port = self.args[0]
        el_type = self.args[-1]

        if el_type == "numb":
            if control_unit.out_condition == 0:
                if control_unit.conditional_jump_buffer != 0:
                    control_unit.data_path.out_acc(False, port)
                control_unit.out_condition = 1
                control_unit.tick()
            elif control_unit.out_condition == 1:
                control_unit.conditional_jump_buffer = control_unit.data_path.read_value()
                control_unit.tick()
                if control_unit.conditional_jump_buffer != 0:
                    control_unit.data_path.out_acc(False, port)
                    control_unit.tick()
        elif el_type == "str":
            if control_unit.out_condition == 0:
                if control_unit.conditional_jump_buffer != 0:
                    control_unit.data_path.out_acc(True, port)
                control_unit.out_condition = 1
                control_unit.tick()
            elif control_unit.out_condition == 1:
                control_unit.conditional_jump_buffer = control_unit.data_path.read_value()
                control_unit.tick()
                if control_unit.conditional_jump_buffer != 0:
                    control_unit.data_path.out_acc(True, port)
                    control_unit.tick()
                    control_unit.data_path.inc_address()
                    control_unit.tick()
        control_unit.select_address(None)
class Halt(Operation):
    def perform(self, control_unit):
        print("End of program by HALT")
        control_unit.program_end_condition = True

opcode = {"mov": Mov(), "add": Add(), "jmp": Jmp(), "jz": Jz(), "in": In(), "out": Out(), "halt": Halt()}
opcode_keys = ["mov", "inc", "dec", "add", "sub", "mul", "div", "jmp", "jz", "jnz", "cmp", "in", "out", "halt"]