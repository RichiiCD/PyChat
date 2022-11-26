
class Log:
    ''' Show custom colored logs in terminal '''

    def __init__(self, color, type, msg):
        self.color = color
        self.type = type
        self.msg = msg

        self.bcolors = {'HEADER': '\033[95m',
                        'OKBLUE': '\033[94m',
                        'OKCYAN': '\033[96m',
                        'OKGREEN': '\033[92m',
                        'WARNING': '\033[93m',
                        'FAIL': '\033[91m',
                        'ENDC': '\033[0m',
                        'BOLD': '\033[1m'}

        self.display()

    def display(self):
        print(f'{self.bcolors["BOLD"] + self.bcolors[self.color]}[{self.type}]{self.bcolors["ENDC"]} {self.msg}')