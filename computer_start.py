from control_unit import ControlUnit

from translator import from_language_to_machine_code, from_machine_code_to_memory
if __name__ == '__main__':

    # file_name = input()
    # f = open(file_name, 'r')
    f = open('tests/prob1.txt', 'r')
    program = f.read()
    from_language_to_machine_code(program)
    f.close()

    f = open('machine_code.txt', 'r')
    machine_code = f.read()
    f.close()
    memory = from_machine_code_to_memory(machine_code, 70)

    f = open('input_for_tests/input_without_data.txt', 'r')
    input_data = f.read()
    input_array = list(input_data)
    input_array.append("\n")
    input_array.append("\0")
    input_array.reverse()

    control_unit = ControlUnit(memory, input_array)
    result = control_unit.start()
    print("".join(result))