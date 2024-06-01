import json
import logging


class CommandError(Exception):
    def __init__(self, *args):
        if args:
            self.message = args[0]
        else:
            self.message = None

    def __str__(self):
        new_message = "CommandError has been raised"
        if self.message:
            new_message = f"CommandError, error in command {self.message} "
        return new_message


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

    def execute(self, control_unit):
        try:
            self.perform(control_unit)
            control_unit.select_address(None)
        except Exception:
            raise CommandError(self.name) from Exception

    def check_register(self, index):
        reg = self.correct_arg(index)
        if reg < 0 or reg > 12:
            raise CommandError(self.name)

    def perform(self, control_unit):
        return

    def correct_arg(self, index):
        new_arg = self.args[index][1:]
        return int(new_arg)


class Lend(Operation):
    def perform(self, control_unit):
        if "r" in self.args[0]:
            self.check_register(0)
            addr = self.correct_arg(0)
            control_unit.data_path.set_left_register_address(addr)
            control_unit.tick()
            addr = self.correct_arg(1)
            control_unit.data_path.set_address(addr)
            control_unit.tick()
            control_unit.data_path.write_value_to_memory(2, None, None, None)
            control_unit.tick()
        if "@" in self.args[0]:
            addr = self.correct_arg(0)
            control_unit.data_path.set_address(addr)
            control_unit.tick()
            self.check_register(1)
            addr = self.correct_arg(1)
            control_unit.data_path.set_left_register_address(addr)
            control_unit.tick()
            control_unit.data_path.write_value_to_register(1, addr, None, None)
            control_unit.tick()


class Mov(Operation):
    def perform(self, control_unit):
        if "r" in self.args[0]:
            self.check_register(0)
            addr = self.correct_arg(0)
            control_unit.data_path.set_left_register_address(addr)
        elif "@" in self.args[0]:
            addr = self.correct_arg(0)
            control_unit.data_path.set_address(addr)
        else:
            raise ValueError("Invalid")
        control_unit.tick()


class Inc(Operation):
    def perform(self, control_unit):
        if "r" in self.args[0]:
            self.check_register(0)
            addr = self.correct_arg(0)
            control_unit.data_path.set_left_register_address(addr)
            control_unit.tick()
            control_unit.data_path.write_value_to_register(0, None, "inc", None)
            control_unit.tick()
        if "@" in self.args[0]:
            addr = self.correct_arg(0)
            control_unit.data_path.set_address(addr)
            control_unit.tick()
            control_unit.data_path.write_value_to_register(2, None, None, None)
            control_unit.tick()
            control_unit.data_path.write_value_to_memory(0, None, "inc", None)
            control_unit.tick()


class Dec(Operation):
    def perform(self, control_unit):
        if "r" in self.args[0]:
            self.check_register(0)
            addr = self.correct_arg(0)
            control_unit.data_path.set_left_register_address(addr)
            control_unit.tick()
            control_unit.data_path.write_value_to_register(0, addr, "dec", None)
            control_unit.tick()
        if "@" in self.args[0]:
            addr = self.correct_arg(0)
            control_unit.data_path.set_address(addr)
            control_unit.tick()
            control_unit.data_path.write_value_to_register(2, None, None, None)
            control_unit.tick()
            control_unit.data_path.write_value_to_memory(0, None, "dec", None)
            control_unit.tick()


class Jmp(Operation):
    def execute(self, control_unit):
        try:
            self.perform(control_unit)
        except Exception:
            raise CommandError(self.name) from Exception

    def perform(self, control_unit):
        next_operation_address = self.correct_arg(0)
        control_unit.select_address(next_operation_address)


class Jz(Operation):
    def execute(self, control_unit):
        try:
            self.perform(control_unit)
        except Exception:
            raise CommandError(self.name) from Exception

    def perform(self, control_unit):
        if control_unit.data_path.zero():
            next_operation_address = self.correct_arg(0)
            control_unit.select_address(next_operation_address)
            control_unit.tick()
            control_unit.data_path.write_value_to_register(0, -5, "dec", None)
            control_unit.tick()
        else:
            control_unit.select_address(None)


class Je(Operation):
    def execute(self, control_unit):
        try:
            self.perform(control_unit)
        except Exception:
            raise CommandError(self.name) from Exception

    def perform(self, control_unit):
        if control_unit.data_path.je_condition():
            next_operation_address = self.correct_arg(0)
            control_unit.select_address(next_operation_address)
            control_unit.tick()
            control_unit.data_path.write_value_to_register(0, -3, "dec", None)
            control_unit.tick()
            control_unit.data_path.write_value_to_register(0, -3, "dec", None)
            control_unit.tick()
        else:
            control_unit.select_address(None)


class Jb(Operation):
    def execute(self, control_unit):
        try:
            self.perform(control_unit)
        except Exception:
            raise CommandError(self.name) from Exception

    def perform(self, control_unit):
        if control_unit.data_path.jb_condition():
            next_operation_address = self.correct_arg(0)
            control_unit.select_address(next_operation_address)
            control_unit.tick()
            control_unit.data_path.write_value_to_register(0, -3, "inc", None)
            control_unit.tick()
        else:
            control_unit.select_address(None)


class Jl(Operation):
    def execute(self, control_unit):
        try:
            self.perform(control_unit)
        except Exception:
            raise CommandError(self.name) from Exception

    def perform(self, control_unit):
        if control_unit.data_path.jl_condition():
            next_operation_address = self.correct_arg(0)
            control_unit.select_address(next_operation_address)
            control_unit.tick()
            control_unit.data_path.write_value_to_register(0, -3, "dec", None)
            control_unit.tick()
        else:
            control_unit.select_address(None)


class Cmp(Operation):
    def perform(self, control_unit):
        if len(self.args) == 2:
            self.check_register(0)
            self.check_register(1)
            addr_1 = self.correct_arg(0)
            addr_2 = self.correct_arg(1)
            control_unit.data_path.set_left_register_address(addr_1)
            control_unit.tick()
            control_unit.data_path.set_right_register_address(addr_2)
            control_unit.tick()
            control_unit.data_path.write_value_to_register(0, -3, "==", None)
            control_unit.tick()
        elif len(self.args) == 4:
            self.check_register(2)
            self.check_register(3)
            mem_addr_1 = self.correct_arg(0)
            mem_addr_2 = self.correct_arg(1)
            reg_addr_1 = self.correct_arg(2)
            reg_addr_2 = self.correct_arg(3)
            control_unit.data_path.set_address(mem_addr_1)
            control_unit.tick()
            control_unit.data_path.set_left_register_address(reg_addr_1)
            control_unit.tick()
            control_unit.data_path.write_value_to_register(2, None, None, None)
            control_unit.tick()
            control_unit.data_path.set_address(mem_addr_2)
            control_unit.tick()
            control_unit.data_path.set_right_register_address(reg_addr_2)
            control_unit.tick()
            control_unit.data_path.write_value_to_register(3, None, None, None)
            control_unit.tick()
            control_unit.data_path.write_value_to_register(0, -3, "==", None)
            control_unit.tick()


class Add(Operation):
    def perform(self, control_unit):
        if len(self.args) >= 5:
            self.check_register(-3)
            self.check_register(-2)
            reg_addr_1 = self.correct_arg(-3)
            reg_addr_2 = self.correct_arg(-2)
            control_unit.data_path.set_left_register_address(reg_addr_1)
            control_unit.tick()
            control_unit.data_path.set_right_register_address(reg_addr_2)
            control_unit.tick()

            mem_addr_1 = self.correct_arg(0)
            control_unit.data_path.set_address(mem_addr_1)
            control_unit.tick()
            control_unit.data_path.write_value_to_register(2, None, None, None)
            control_unit.tick()

            for i in range(1, len(self.args) - 3):
                mem_addr = self.correct_arg(i)
                control_unit.data_path.set_address(mem_addr)
                control_unit.tick()
                control_unit.data_path.write_value_to_register(3, None, None, None)
                control_unit.tick()
                control_unit.data_path.write_value_to_register(0, None, "+", None)
                control_unit.tick()
            mem_addr_result = self.correct_arg(-1)
            control_unit.data_path.set_address(mem_addr_result)
            control_unit.data_path.write_value_to_memory(2, None, None, None)


class Sub(Operation):
    def perform(self, control_unit):
        if len(self.args) >= 5:
            self.check_register(-3)
            self.check_register(-2)
            reg_addr_1 = self.correct_arg(-3)
            reg_addr_2 = self.correct_arg(-2)
            control_unit.data_path.set_left_register_address(reg_addr_1)
            control_unit.tick()
            control_unit.data_path.set_right_register_address(reg_addr_2)
            control_unit.tick()

            mem_addr_1 = self.correct_arg(0)
            control_unit.data_path.set_address(mem_addr_1)
            control_unit.tick()
            control_unit.data_path.write_value_to_register(2, None, None, None)
            control_unit.tick()

            for i in range(1, len(self.args) - 3):
                mem_addr = self.correct_arg(i)
                control_unit.data_path.set_address(mem_addr)
                control_unit.tick()
                control_unit.data_path.write_value_to_register(3, None, None, None)
                control_unit.tick()
                control_unit.data_path.write_value_to_register(0, None, "-", None)
                control_unit.tick()
            mem_addr_result = self.correct_arg(-1)
            control_unit.data_path.set_address(mem_addr_result)
            control_unit.data_path.write_value_to_memory(2, None, None, None)


class Mul(Operation):
    def perform(self, control_unit):
        if len(self.args) >= 5:
            self.check_register(-3)
            self.check_register(-2)
            reg_addr_1 = self.correct_arg(-3)
            reg_addr_2 = self.correct_arg(-2)
            control_unit.data_path.set_left_register_address(reg_addr_1)
            control_unit.tick()
            control_unit.data_path.set_right_register_address(reg_addr_2)
            control_unit.tick()

            mem_addr_1 = self.correct_arg(0)
            control_unit.data_path.set_address(mem_addr_1)
            control_unit.tick()
            control_unit.data_path.write_value_to_register(2, None, None, None)
            control_unit.tick()

            for i in range(1, len(self.args) - 3):
                mem_addr = self.correct_arg(i)
                control_unit.data_path.set_address(mem_addr)
                control_unit.tick()
                control_unit.data_path.write_value_to_register(3, None, None, None)
                control_unit.tick()
                control_unit.data_path.write_value_to_register(0, None, "*", None)
                control_unit.tick()
            mem_addr_result = self.correct_arg(-1)
            control_unit.data_path.set_address(mem_addr_result)
            control_unit.data_path.write_value_to_memory(2, None, None, None)


class Div(Operation):
    def perform(self, control_unit):
        if len(self.args) >= 5:
            self.check_register(-3)
            self.check_register(-2)
            reg_addr_1 = self.correct_arg(-3)
            reg_addr_2 = self.correct_arg(-2)
            control_unit.data_path.set_left_register_address(reg_addr_1)
            control_unit.tick()
            control_unit.data_path.set_right_register_address(reg_addr_2)
            control_unit.tick()

            mem_addr_1 = self.correct_arg(0)
            control_unit.data_path.set_address(mem_addr_1)
            control_unit.tick()
            control_unit.data_path.write_value_to_register(2, None, None, None)
            control_unit.tick()

            for i in range(1, len(self.args) - 3):
                mem_addr = self.correct_arg(i)
                control_unit.data_path.set_address(mem_addr)
                control_unit.tick()
                control_unit.data_path.write_value_to_register(3, None, None, None)
                control_unit.tick()
                control_unit.data_path.write_value_to_register(0, None, "/", None)
                control_unit.tick()
            mem_addr_result = self.correct_arg(-1)
            control_unit.data_path.set_address(mem_addr_result)
            control_unit.data_path.write_value_to_memory(2, None, None, None)


class Rmd(Operation):
    def perform(self, control_unit):
        if len(self.args) == 3:
            self.check_register(0)
            self.check_register(1)
            addr_1 = self.correct_arg(0)
            addr_2 = self.correct_arg(1)
            control_unit.data_path.set_left_register_address(addr_1)
            control_unit.tick()
            control_unit.data_path.set_right_register_address(addr_2)
            control_unit.tick()
            control_unit.data_path.write_value_to_register(0, None, "==", None)
            control_unit.tick()
            mem_addr = self.correct_arg(2)
            control_unit.data_path.set_address(mem_addr)
            control_unit.tick()
            control_unit.data_path.write_value_to_memory(2, None, None, None)
            control_unit.tick()
        elif len(self.args) == 5:
            self.check_register(2)
            self.check_register(3)
            mem_addr_1 = self.correct_arg(0)
            mem_addr_2 = self.correct_arg(1)
            reg_addr_1 = self.correct_arg(2)
            reg_addr_2 = self.correct_arg(3)
            control_unit.data_path.set_address(mem_addr_1)
            control_unit.tick()
            control_unit.data_path.set_left_register_address(reg_addr_1)
            control_unit.tick()
            control_unit.data_path.write_value_to_register(2, None, None, None)
            control_unit.tick()
            control_unit.data_path.set_address(mem_addr_2)
            control_unit.tick()
            control_unit.data_path.set_right_register_address(reg_addr_2)
            control_unit.tick()
            control_unit.data_path.write_value_to_register(3, None, None, None)
            control_unit.tick()
            control_unit.data_path.write_value_to_register(0, None, "%", None)
            control_unit.tick()
            mem_addr = self.correct_arg(4)
            control_unit.data_path.set_address(mem_addr)
            control_unit.tick()
            control_unit.data_path.write_value_to_memory(2, None, None, None)
            control_unit.tick()


class In(Operation):
    def perform(self, control_unit):
        if len(self.args) == 2:
            addr = self.correct_arg(1)
            control_unit.data_path.set_address(addr)
            control_unit.tick()
            port = self.args[0]
            control_unit.data_path.write_value_to_register(0, -4, "1", None)
            control_unit.tick()

            while not control_unit.data_path.zero():
                control_unit.data_path.write_value_to_memory(-1, None, None, port)
                control_unit.tick()
                control_unit.data_path.write_value_to_register(1, -5, None, None)
                control_unit.tick()
                if control_unit.data_path.registers[-5] == 10:
                    enter = "\\n"
                    logging.debug(f'input: "{enter}"')
                elif control_unit.data_path.registers[-5] != 0:
                    logging.debug(f'input: "{chr(control_unit.data_path.registers[-5])}"')
                control_unit.data_path.inc_address()
                control_unit.tick()
            control_unit.data_path.write_value_to_register(0, -5, "dec", None)
            control_unit.data_path.set_address(addr)
            control_unit.tick()
        else:
            port = self.args[0]
            control_unit.data_path.write_value_to_register(0, -4, "0", None)
            control_unit.tick()
            control_unit.data_path.write_value_to_register(-1, None, None, port)
            control_unit.tick()
            if control_unit.data_path.registers[-5] == 10:
                enter = "\\n"
                logging.debug(f'input: "{enter}"')
            elif control_unit.data_path.registers[-5] != 0:
                logging.debug(f'input: "{chr(control_unit.data_path.registers[-5])}"')


class Out(Operation):
    def perform(self, control_unit):
        port = self.args[0]
        el_type = self.args[-1]
        output = "".join(control_unit.data_path.buffer[1]).replace("\n", "\\n")

        if el_type == "numb":
            self.perform_for_numb(control_unit, output, port)
        elif el_type == "str":
            self.perform_for_str(control_unit, output, port)

    def perform_for_numb(self, control_unit, output, port):
        if control_unit.data_path.registers[-4] == 0:
            logging.debug(f'out: "{output}" << "{control_unit.data_path.registers[-5]}"')
            control_unit.data_path.out_register(False, port)
            control_unit.tick()
            control_unit.data_path.write_value_to_register(0, -4, "1", None)
            control_unit.tick()
        elif control_unit.data_path.registers[-4] == 1:
            control_unit.data_path.write_value_to_register(1, -5, None, None)
            control_unit.tick()
            logging.debug(f'out: "{output}" << "{control_unit.data_path.registers[-5]}"')
            control_unit.data_path.out_register(False, port)
            control_unit.tick()

    def perform_for_str(self, control_unit, output, port):
        if control_unit.data_path.registers[-4] == 0:
            if not control_unit.data_path.zero():
                self.correct_out(output, control_unit)
                control_unit.data_path.out_register(True, port)
                control_unit.tick()
            control_unit.data_path.write_value_to_register(0, -4, "1", None)
            control_unit.tick()
        elif control_unit.data_path.registers[-4] == 1:
            control_unit.data_path.write_value_to_register(1, -5, None, None)
            control_unit.tick()
            if not control_unit.data_path.zero():
                self.correct_out(output, control_unit)
                control_unit.data_path.out_register(True, port)
                control_unit.tick()
                control_unit.data_path.inc_address()
                control_unit.tick()

    def correct_out(self, output, control_unit):
        if control_unit.data_path.registers[-5] == 10:
            enter = "\\n"
            logging.debug(f'out: "{output}" << "{enter}"')
        elif control_unit.data_path.registers[-5] != 0:
            logging.debug(f'out: "{output}" << "{chr(control_unit.data_path.registers[-5])}"')


class Halt(Operation):
    def perform(self, control_unit):
        control_unit.program_end_condition = True


opcode = {
    "lend": Lend(),
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
    "lend",
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
