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
        elif len(self.args) == 3:
            control_unit.data_path.set_address(self.args[0])
            control_unit.tick()
            control_unit.data_path.write_value_to_acc(1, None, None)
            control_unit.tick()
            control_unit.data_path.set_address(self.args[-1])
            control_unit.tick()
            control_unit.data_path.write_value_to_memory(1, None, None)
            control_unit.tick()
            control_unit.data_path.set_address(self.args[1])
            control_unit.tick()
            control_unit.data_path.write_value_to_acc(1, None, None)
            control_unit.tick()
            control_unit.data_path.set_address(self.args[0])
            control_unit.tick()
            control_unit.data_path.write_value_to_memory(1, None, None)
            control_unit.tick()
            control_unit.data_path.set_address(self.args[-1])
            control_unit.tick()
            control_unit.data_path.write_value_to_acc(1, None, None)
            control_unit.tick()
            control_unit.data_path.set_address(self.args[1])
            control_unit.tick()
            control_unit.data_path.write_value_to_memory(1, None, None)
            control_unit.tick()

        control_unit.select_address(None)
class Inc(Operation):
    def perform(self, control_unit):
        control_unit.data_path.set_address(self.args[0])
        control_unit.tick()
        control_unit.data_path.write_value_to_acc(1, None, None)
        control_unit.tick()
        control_unit.data_path.write_value_to_memory(0, "inc", None)
        control_unit.tick()
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
class Je(Operation):
    def perform(self, control_unit):
        if control_unit.je_condition == 1:
            next_operation_address = self.args[0]
            control_unit.select_address(next_operation_address)
            control_unit.je_condition = 0
            control_unit.tick()
        else:
            control_unit.select_address(None)
class Cmp(Operation):
    def perform(self, control_unit):
        first_address = self.args[0]
        control_unit.data_path.set_address(first_address)
        control_unit.tick()
        control_unit.data_path.write_value_to_acc(1, None, None)
        control_unit.tick()

        adds = self.args[1]
        control_unit.data_path.set_address(adds)
        control_unit.tick()
        control_unit.je_condition = control_unit.data_path.write_value_to_acc(0, "==", None)
        control_unit.tick()
        control_unit.select_address(None)
class Add(Operation):
    def perform(self, control_unit):
        first_address = self.args[0]
        control_unit.data_path.set_address(first_address)
        control_unit.tick()

        control_unit.data_path.write_value_to_acc(1, None, None)
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
class Rmd(Operation):
    def perform(self, control_unit):
        first_address = self.args[0]
        control_unit.data_path.set_address(first_address)
        control_unit.tick()
        control_unit.data_path.write_value_to_acc(1, None, None)
        control_unit.tick()

        adds = self.args[1]
        control_unit.data_path.set_address(adds)
        control_unit.tick()
        control_unit.data_path.write_value_to_acc(0, "%", None)
        control_unit.tick()

        last_address = self.args[-1]
        control_unit.data_path.set_address(last_address)
        control_unit.tick()
        control_unit.data_path.write_value_to_memory(1, None, None)
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
                control_unit.conditional_jump_buffer = control_unit.data_path.write_value_to_acc(1, None, None)
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
                control_unit.conditional_jump_buffer = control_unit.data_path.write_value_to_acc(1, None, None)
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

opcode = {"mov": Mov(), "inc": Inc(), "add": Add(), "rmd": Rmd(), "jmp": Jmp(), "jz": Jz(), "je": Je(), "cmp": Cmp(), "in": In(), "out": Out(), "halt": Halt()}
opcode_keys = ["mov", "inc", "dec", "add", "sub", "mul", "div", "rmd", "jmp", "jz", "je", "cmp", "in", "out", "halt"]