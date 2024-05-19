import json

from translator import from_language_to_machine_code
if __name__ == '__main__':
    # file_name = input()
    # f = open(file_name, 'r')
    f = open('tests/test_1.txt', 'r')
    program = f.read()
    from_language_to_machine_code(program)
    f.close()

    # f = open('machine_code.txt', 'r')
    # machine_code = f.read()
    # test = json.loads(machine_code)
    # print(test[0]['arg'][0])