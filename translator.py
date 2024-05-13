import re
from isa import opcode

def write_str_to_memory(str_data, machine_code, index):
    for i in str_data:
        machine_code += f"{{'index': {str(index)}, 'type': 'string', 'data': "
        if i == "$":
            machine_code += f"{0}}},\n"
        else:
            machine_code += f"{ord(i)}}},\n"
        index += 1
    return machine_code[:-3], index

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
                    machine_code += f"{{'index': {str(index)}, 'operation': '{data[j]}'"
                    if j == len(data) - 1:
                        machine_code += "},\n"
                        break
                    elif data[j + 1] in opcode:
                        machine_code += "}, "
                        index += 1
                    else:
                        machine_code += ", 'arg': ["
                elif ":" in data[j]:
                    labels[data[j][:-1]] = index
                else:
                    new_el = re.sub(r',', '', data[j])
                    try:
                        float(new_el)
                        machine_code += f"{new_el}"
                    except ValueError:
                        machine_code += f"'{new_el}'"

                    if data[j + 1] in opcode or ":" in data[j + 1]:
                        machine_code += "]},\n"
                        index += 1
                    else:
                        machine_code += ", "
            break

    starting_data_index = index + 1

    # Записываем все данные
    i = 1
    while True:
        index += 1
        if data[i + 1] == "number":
            machine_code += f"{{'index': {index}, 'type': 'number', 'data': "
            machine_code += f"{data[i + 2]}"
        else:
            str_data = ""
            while "$" not in data[i + 2]:
                str_data += f"{data[i + 2]} "
                i += 1
            else:
                str_data += f"{data[i + 2]}"

            machine_code, index = write_str_to_memory(str_data, machine_code, index)

        if data[i + 3] == ".code:":
            machine_code += "}]"
            break
        else:
            machine_code += "},\n"
        i += 3

    # Заменяем все регистры на адреса в памяти
    all_registers = re.findall(r"[R\d]{2,}", machine_code)
    for i in all_registers:
        old_index = re.search("\d{1,}", i).group(0)
        new_index = str(starting_data_index + int(old_index))
        machine_code = re.sub(f"'R{old_index}'", new_index, machine_code)

    # Заменяем все лейблы на адреса команд
    for i in list(labels.keys()):
        machine_code = re.sub(f"'{i}'", str(labels[i]), machine_code)

    f = open("machine_code.txt", "w+")
    f.write(machine_code)
    f.close()

    print(data)
    print(machine_code)