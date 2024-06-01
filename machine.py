import logging
import sys

from control_unit import ControlUnit
from isa import from_machine_code_to_memory


def main(target, input_file):
    memory = from_machine_code_to_memory(target, 70)

    f = open(input_file)
    input_data = f.read()
    f.close()
    input_array = list(input_data)
    input_array.append("\n")
    input_array.append("\0")
    input_array.reverse()

    logging.basicConfig(level=logging.DEBUG, filename="log_message.log", filemode="w")

    control_unit = ControlUnit(memory, input_array)
    result = control_unit.start(10000)
    str_result = "".join(result)
    f = open("result.txt", "w+")
    f.write(str_result)
    f.close()
    print(str_result)


if __name__ == "__main__":
    assert len(sys.argv) == 3, "Wrong arguments: machine.py <code_file> <input_file>"
    _, code_file, input_file = sys.argv
    main(code_file, input_file)
