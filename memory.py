class Memory:

    def __init__(self):
        self.memory = {}

    def init_memory(self, limit: int):
        for i in range(limit):
            addres = "r" + str(i)
            self.memory[addres] = 0