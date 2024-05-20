from control_unit import ControlUnit

from translator import from_language_to_machine_code, from_machine_code_to_memory
if __name__ == '__main__':
    # file_name = input()
    # f = open(file_name, 'r')
    f = open('tests/test_2.txt', 'r')
    program = f.read()
    from_language_to_machine_code(program)
    f.close()

    f = open('machine_code.txt', 'r')
    machine_code = f.read()
    memory = from_machine_code_to_memory(machine_code, 20)
    print(memory)

    control_unit = ControlUnit(memory)
    control_unit.start()