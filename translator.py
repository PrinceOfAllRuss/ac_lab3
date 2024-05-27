import re
from isa import opcode_keys

def write_str_to_memory(str_data, machine_code, index):
    for i in str_data:
        if i == "$":
            enter = ord("\n")
            machine_code += f'{{"index": {str(index)}, "data": {enter}}},\n'
        else:
            machine_code += f'{{"index": {str(index)}, "data": {ord(i)}}},\n'
        index += 1
    machine_code += f'{{"index": {str(index + 1)}, "data": {0}'

    return machine_code, index

def from_language_to_machine_code(program: str):
    lines_of_code = len(program.split("\n"))
    program = re.sub("\s{2}", "", program)
    data = re.split("\s", program)
    # raise EOFError(program, data)


    labels = {}
    machine_code = "["
    index = 0

    # Записываем все команды
    for i in range(len(data)):
        if data[i] == ".code:":
            for j in range(i + 1, len(data)):
                if data[j] in opcode_keys:
                    machine_code += f'{{"index": {index}, "operation": "{data[j]}"'
                    if j == len(data) - 1:
                        machine_code += "},\n"
                        break
                    elif data[j + 1] in opcode_keys:
                        machine_code += "},\n"
                        index += 1
                    else:
                        if data[j] not in ["halt"]:
                            machine_code += ', "arg": ['
                        else:
                            machine_code += "},\n"
                            index += 1
                elif ":" in data[j]:
                    labels[data[j][:-1]] = index
                else:
                    new_el = re.sub(r',', '', data[j])
                    if re.search(r'[a-zA-Z]', new_el) is None:
                        machine_code += f'{new_el}'
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
            break

    instr_count = index

    # Записываем все данные
    if data[0] == ".data:":
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
            machine_code = re.sub(f'"{i}"', f'{new_index}', machine_code)
    else:
        machine_code = f'{machine_code[:-2]}]'

    # Заменяем все лейблы на адреса команд
    all_labels = list(labels.keys())
    for i in all_labels:
        machine_code = re.sub(f'"{i}"', f'{labels[i]}', machine_code)

    print("source LoC:", lines_of_code, "code instr:", instr_count)
    print("============================================================")

    return machine_code

def main(source, target):
    f = open(source, 'r')
    program = f.read()
    f.close()

    machine_code = from_language_to_machine_code(program)

    with open(target, "w", encoding="utf-8") as file:
        file.write(machine_code)