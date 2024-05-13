from translator import from_language_to_machine_code
if __name__ == '__main__':
    f = open('tests/test_1.txt', 'r')
    program = f.read()
    from_language_to_machine_code(program)
    f.close()