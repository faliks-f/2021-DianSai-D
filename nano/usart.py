import serial

check_send = [0X75, 0XBB, 0X00, 0X8A, 0XBB]
check_read = [0X75, 0XAA, 0X00, 0X8A, 0XAA]
task1 = [0X75, 0XAA, 0X01, 0X8A, 0XAB]
task2 = [0X75, 0XAA, 0X02, 0X8A, 0XAC]
task3 = [0X75, 0XAA, 0X03, 0X8A, 0XAD]
task4 = [0X75, 0XAA, 0X04, 0X8A, 0XAE]
complete = [0X75, 0XBB, 0X01, 0X8A, 0XBC]


class Usart:
    def __init__(self):
        self.usart = serial.Serial("COM5", 115200, timeout=0)

    def write(self, command):
        self.usart.write(bytearray(command))

    def read(self):
        res2 = self.usart.read(5)
        return res2

    @staticmethod
    def compare(command1, command2):
        if len(command1) < 5:
            return False
        if command1[0] == command2[0] and command1[1] == command2[1] and \
                command1[2] == command2[2] and command1[3] == command2[3] and \
                command1[4] == command2[4]:
            return True
        else:
            return False

    def check_write(self):
        self.write(check_send)

    def check_read(self):
        res = self.read()
        if len(res) < 5:
            return False
        return self.compare(res, check_read)

    def complete_write(self):
        self.write(complete)

    def get_result(self):
        res1 = self.read()
        if res1 is None:
            return 0
        if len(res1) < 5:
            return 0
        print(res1)
        if self.compare(res1, task1):
            return 1
        elif self.compare(res1, task2):
            return 2
        elif self.compare(res1, task3):
            return 3
        elif self.compare(res1, task4):
            return 4
        return 0
