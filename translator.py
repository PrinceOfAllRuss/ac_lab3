import re
import sys

from isa import opcode_keys


def write_str_to_memory(str_data, machine_code, index):
    for i in str_data:
        if i == "$":
            enter = ord("\n")
            machine_code += f'{{"index": {index!s}, "data": {enter}}},\n'
        else:
            machine_code += f'{{"index": {index!s}, "data": {ord(i)}}},\n'
        index += 1
    machine_code += f'{{"index": {index + 1!s}, "data": {0}'

    return machine_code, index
def get_variable_name(data, i):
    if data[i + 1].count('"') == 2:
        str_data = re.sub('"', "", data[i + 1])
    else:
        str_data = f"{data[i + 1]} "[1:]
        i += 1
        while '"' not in data[i + 1]:
            str_data += f"{data[i + 1]} "
            i += 1
        else:
            str_data += f"{data[i + 1]}"[:-1]
    return str_data, i
def get_command_args(machine_code, index, data, j):
    new_el = re.sub(r",", "", data[j])
    if re.search(r"[a-zA-Z]", new_el) is None:
        machine_code += f"{new_el}"
    else:
        machine_code += f'"{new_el}"'

    if j == len(data) - 1:
        machine_code += "]},\n"
    else:
        if data[j + 1] in opcode_keys or ":" in data[j + 1]:
            machine_code += "]},\n"
            index += 1
        else:
            machine_code += ", "
    return machine_code, index
def get_command(machine_code, index, data, j):
    machine_code += f'{{"index": {index}, "operation": "{data[j]}"'
    if j == len(data) - 1:
        machine_code += "},\n"
    elif data[j + 1] in opcode_keys:
        machine_code += "},\n"
        index += 1
    else:
        if data[j] not in ["halt"]:
            machine_code += ', "arg": ['
        else:
            machine_code += "},\n"
            index += 1
    return machine_code, index
def get_all_commands(labels, machine_code, index, data):
    for i in range(len(data)):
        if data[i] == ".code:":
            for j in range(i + 1, len(data)):
                if data[j] in opcode_keys:
                    machine_code, index = get_command(machine_code, index, data, j)
                elif ":" in data[j]:
                    labels[data[j][:-1]] = index
                else:
                    machine_code, index = get_command_args(machine_code, index, data, j)
            break
    return labels, machine_code, index
def get_all_data(machine_code, index, data):
    if data[0] == ".data:":
        dict_for_variable_names = {}
        i = 1
        while data[i] != ".code:":
            index += 1
            if '"' not in data[i + 1]:
                machine_code += f'{{"index": {index}, "data": '
                machine_code += f"{data[i + 1]}"
                dict_for_variable_names[data[i]] = index
            else:
                dict_for_variable_names[data[i]] = index

                str_data, i = get_variable_name(data, i)

                machine_code, index = write_str_to_memory(str_data, machine_code, index)

            if data[i + 2] == ".code:":
                machine_code += "}]"
            else:
                machine_code += "},\n"
            i += 2

        # Заменяем все регистры на адреса в памяти
        all_registers = list(dict_for_variable_names.keys())
        for i in all_registers:
            new_index = dict_for_variable_names[i]
            machine_code = re.sub(f'"{i}"', f"{new_index}", machine_code)
    else:
        machine_code = f"{machine_code[:-2]}]"
    return machine_code, index
def from_language_to_machine_code(program: str):
    lines_of_code = len(program.split("\n"))
    program = re.sub("\\s*;\\s*.*\\s*\n", "\n", program)
    program = re.sub(r"\s{2}", "", program)
    data = re.split(r"\s", program)

    labels = {}
    machine_code = "["
    index = 0
    # Записываем все команды
    labels, machine_code, index = get_all_commands(labels, machine_code, index, data)
    instr_count = index
    # Записываем все данные
    machine_code, index = get_all_data(machine_code, index, data)

    # Заменяем все лейблы на адреса команд
    all_labels = list(labels.keys())
    for i in all_labels:
        machine_code = re.sub(f'"{i}"', f"{labels[i]}", machine_code)

    print("source LoC:", lines_of_code, "code instr:", instr_count + 1)
    print("============================================================")

    return machine_code

def main(source, target):
    f = open(source)
    program = f.read()
    f.close()

    machine_code = from_language_to_machine_code(program)

    with open(target, "w", encoding="utf-8") as file:
        file.write(machine_code)

if __name__ == "__main__":
    assert len(sys.argv) == 3, "Wrong arguments: translator.py <code_file> <machine_code_file>"
    _, source, target = sys.argv
    main(source, target)
