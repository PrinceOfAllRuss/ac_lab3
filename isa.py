import json
import logging


def from_machine_code_to_memory(target, memory_size):
    f = open(target)
    machine_code = f.read()
    f.close()
    machine_array = json.loads(machine_code)
    if len(machine_array) > memory_size:
        raise OverflowError
    memory = [0] * memory_size
    for i in range(len(machine_array)):
        obj = machine_array[i]
        keys = list(obj.keys())
        index = obj["index"]
        if keys[1] == "data":
            memory[index] = obj["data"]
        else:
            if "arg" in keys:
                operation = Operation(obj["operation"], obj["arg"])
            else:
                operation = Operation(obj["operation"], [])
            memory[index] = operation
    return memory


class Operation:
    def __init__(self, name="", args=[]):
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


class Dec(Operation):
    def perform(self, control_unit):
        control_unit.data_path.set_address(self.args[0])
        control_unit.tick()
        control_unit.data_path.write_value_to_acc(1, None, None)
        control_unit.tick()
        control_unit.data_path.write_value_to_memory(0, "dec", None)
        control_unit.tick()
        control_unit.select_address(None)


class Jmp(Operation):
    def perform(self, control_unit):
        next_operation_address = self.args[0]
        control_unit.select_address(next_operation_address)


class Jz(Operation):
    def perform(self, control_unit):
        if control_unit.data_path.zero():
            next_operation_address = self.args[0]
            control_unit.select_address(next_operation_address)
            control_unit.tick()
            control_unit.data_path.write_value_to_acc(0, "dec", None)
            control_unit.tick()
        else:
            control_unit.select_address(None)


class Je(Operation):
    def perform(self, control_unit):
        if control_unit.data_path.je_condition():
            next_operation_address = self.args[0]
            control_unit.select_address(next_operation_address)
            control_unit.tick()
            control_unit.data_path.write_value_to_acc(0, "dec", None)
            control_unit.tick()
            control_unit.data_path.write_value_to_acc(0, "dec", None)
            control_unit.tick()
        else:
            control_unit.select_address(None)


class Jb(Operation):
    def perform(self, control_unit):
        if control_unit.data_path.jb_condition():
            next_operation_address = self.args[0]
            control_unit.select_address(next_operation_address)
            control_unit.tick()
            control_unit.data_path.write_value_to_acc(0, "inc", None)
            control_unit.tick()
        else:
            control_unit.select_address(None)


class Jl(Operation):
    def perform(self, control_unit):
        if control_unit.data_path.jl_condition():
            next_operation_address = self.args[0]
            control_unit.select_address(next_operation_address)
            control_unit.tick()
            control_unit.data_path.write_value_to_acc(0, "dec", None)
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
        control_unit.data_path.write_value_to_acc(0, "==", None)
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

        control_unit.data_path.write_value_to_memory(1, None, None)
        control_unit.tick()

        control_unit.select_address(None)


class Sub(Operation):
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

            control_unit.data_path.write_value_to_acc(0, "-", None)
            control_unit.tick()

        last_address = self.args[-1]
        control_unit.data_path.set_address(last_address)
        control_unit.tick()

        control_unit.data_path.write_value_to_memory(1, None, None)
        control_unit.tick()

        control_unit.select_address(None)


class Mul(Operation):
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

            control_unit.data_path.write_value_to_acc(0, "*", None)
            control_unit.tick()

        last_address = self.args[-1]
        control_unit.data_path.set_address(last_address)
        control_unit.tick()

        control_unit.data_path.write_value_to_memory(1, None, None)
        control_unit.tick()

        control_unit.select_address(None)


class Div(Operation):
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

            control_unit.data_path.write_value_to_acc(0, "/", None)
            control_unit.tick()

        last_address = self.args[-1]
        control_unit.data_path.set_address(last_address)
        control_unit.tick()

        control_unit.data_path.write_value_to_memory(1, None, None)
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
            control_unit.tick()
            port = self.args[0]
            control_unit.out_condition_register = 1
            control_unit.tick()

            while not control_unit.data_path.zero():
                control_unit.data_path.write_value_to_memory(-1, None, port)
                control_unit.tick()
                control_unit.data_path.write_value_to_acc(1, None, None)
                control_unit.tick()
                if control_unit.data_path.acc == 10:
                    enter = "\\n"
                    logging.debug(f'input: "{enter}"')
                elif control_unit.data_path.acc != 0:
                    logging.debug(f'input: "{chr(control_unit.data_path.acc)}"')
                control_unit.data_path.inc_address()
                control_unit.tick()
            control_unit.data_path.write_value_to_acc(0, "dec", None)
            control_unit.data_path.set_address(addr)
            control_unit.tick()
        else:
            port = self.args[0]
            control_unit.out_condition_register = 0
            control_unit.tick()
            control_unit.data_path.write_value_to_acc(-1, None, port)
            control_unit.tick()
            if control_unit.data_path.acc == 10:
                enter = "\\n"
                logging.debug(f'input: "{enter}"')
            elif control_unit.data_path.acc != 0:
                logging.debug(f'input: "{chr(control_unit.data_path.acc)}"')

        control_unit.select_address(None)


class Out(Operation):
    def perform(self, control_unit):
        port = self.args[0]
        el_type = self.args[-1]
        output = "".join(control_unit.data_path.buffer[1]).replace("\n", "\\n")

        if el_type == "numb":
            self.perform_for_numb(control_unit, output, port)
        elif el_type == "str":
            self.perform_for_str(control_unit, output, port)
        control_unit.select_address(None)

    def perform_for_numb(self, control_unit, output, port):
        if control_unit.out_condition_register == 0:
            if not control_unit.data_path.zero():
                logging.debug(f'out: "{output}" << "{control_unit.data_path.acc}"')
                control_unit.data_path.out_acc(False, port)
                control_unit.tick()
            control_unit.out_condition_register = 1
            control_unit.tick()
        elif control_unit.out_condition_register == 1:
            control_unit.data_path.write_value_to_acc(1, None, None)
            control_unit.tick()
            if not control_unit.data_path.zero():
                logging.debug(f'out: "{output}" << "{control_unit.data_path.acc}"')
                control_unit.data_path.out_acc(False, port)
                control_unit.tick()

    def perform_for_str(self, control_unit, output, port):
        if control_unit.out_condition_register == 0:
            if not control_unit.data_path.zero():
                self.correct_out(output, control_unit)
                control_unit.data_path.out_acc(True, port)
                control_unit.tick()
            control_unit.out_condition_register = 1
            control_unit.tick()
        elif control_unit.out_condition_register == 1:
            control_unit.data_path.write_value_to_acc(1, None, None)
            control_unit.tick()
            if not control_unit.data_path.zero():
                self.correct_out(output, control_unit)
                control_unit.data_path.out_acc(True, port)
                control_unit.tick()
                control_unit.data_path.inc_address()
                control_unit.tick()

    def correct_out(self, output, control_unit):
        if control_unit.data_path.acc == 10:
            enter = "\\n"
            logging.debug(f'out: "{output}" << "{enter}"')
        elif control_unit.data_path.acc != 0:
            logging.debug(f'out: "{output}" << "{chr(control_unit.data_path.acc)}"')


class Halt(Operation):
    def perform(self, control_unit):
        control_unit.program_end_condition = True


opcode = {
    "mov": Mov(),
    "inc": Inc(),
    "dec": Dec(),
    "add": Add(),
    "sub": Sub(),
    "mul": Mul(),
    "div": Div(),
    "rmd": Rmd(),
    "jmp": Jmp(),
    "jz": Jz(),
    "je": Je(),
    "jb": Jb(),
    "jl": Jl(),
    "cmp": Cmp(),
    "in": In(),
    "out": Out(),
    "halt": Halt(),
}
opcode_keys = [
    "mov",
    "inc",
    "dec",
    "add",
    "sub",
    "mul",
    "div",
    "rmd",
    "jmp",
    "jz",
    "je",
    "jb",
    "jl",
    "cmp",
    "in",
    "out",
    "halt",
]
