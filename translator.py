import re
from isa import opcode
def from_language_to_machine_code(program: str):
    program = re.sub("\s{4}", "", program)
    data = re.split("\s", program)

    if data[-1] != "halt":
        raise Exception("Program without 'half'")

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
                else:
                    new_el = re.sub(r'[,]', '', data[j])
                    machine_code += f"'{new_el}'"
                    if data[j + 1] in opcode:
                        machine_code += "]},\n"
                        index += 1
                    else:
                        machine_code += ", "

    starting_data_index = index + 1

    # Записываем все данные
    i = 1
    while True:
        index += 1
        machine_code += f"{{'index': {str(index)}, 'data': "
        if data[i + 1] == "number":
            machine_code += f"{str(data[i + 2])}"
        else:
            # TODO
            machine_code += f"'{data[i + 2]}'"

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

    print(data)
    print(machine_code)