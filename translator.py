import json
import re
from isa import opcode, Operation

def write_str_to_memory(str_data, machine_code, index):
    for i in str_data:
        machine_code += f'{{"index": {str(index)}, "data": {ord(i)}}},\n'
        index += 1
    machine_code += f'{{"index": {str(index)}, "data": {0}'

    return machine_code, index

def from_language_to_machine_code(program: str):
    program = re.sub("\s{4}", "", program)
    data = re.split("\s", program)

    labels = {}
    machine_code = "["
    index = 0

    # Записываем все команды
    for i in range(len(data)):
        if data[i] == ".code:":
            for j in range(i + 1, len(data)):
                if data[j] in opcode:
                    machine_code += f'{{"index": {index}, "operation": "{data[j]}"'
                    if j == len(data) - 1:
                        machine_code += "},\n"
                        break
                    elif data[j + 1] in opcode:
                        machine_code += "}, "
                        index += 1
                    else:
                        machine_code += ', "arg": ['
                elif ":" in data[j]:
                    labels[data[j][:-1]] = index
                else:
                    new_el = re.sub(r',', '', data[j])
                    if "@" in new_el:
                        machine_code += f'{new_el}'
                    else:
                        machine_code += f'{new_el}'

                    if data[j + 1] in opcode or ":" in data[j + 1]:
                        machine_code += "]},\n"
                        index += 1
                    else:
                        machine_code += ", "
            break

    # Записываем все данные
    dict_for_variable_names = {}
    i = 1
    while True:
        index += 1
        if "\"" not in data[i + 1]:
            machine_code += f'{{"index": {index}, "data": '
            machine_code += f"{data[i + 1]}"
            dict_for_variable_names[data[i]] = index
        else:
            dict_for_variable_names[data[i]] = index
            if data[i + 1].count("\"") == 2:
                str_data = re.sub("\"", "", data[i + 1])
            else:
                str_data = f"{data[i + 1]} "[1:]
                i += 1
                while "\"" not in data[i + 1]:
                    str_data += f"{data[i + 1]} "
                    i += 1
                else:
                    str_data += f"{data[i + 1]}"[:-1]

            machine_code, index = write_str_to_memory(str_data, machine_code, index)

        if data[i + 2] == ".code:":
            machine_code += "}]"
            break
        else:
            machine_code += "},\n"
        i += 2

    # Заменяем все регистры на адреса в памяти
    all_registers = list(dict_for_variable_names.keys())
    for i in all_registers:
        new_index = dict_for_variable_names[i]
        machine_code = re.sub(f'@{i}', f'"@{new_index}"', machine_code)
        machine_code = re.sub(f'{i}', f'{new_index}', machine_code)

    # Заменяем все лейблы на адреса команд
    all_labels = list(labels.keys())
    for i in all_labels:
        machine_code = re.sub(f'{i}', f'"@{labels[i]}"', machine_code)

    f = open("machine_code.txt", "w+")
    f.write(machine_code)
    f.close()

    # print(data)
    print(machine_code)

def from_machine_code_to_memory(machine_code, memory_size):
    machine_array = json.loads(machine_code)
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