from colorama import Fore, init
from functions.modbustcp import TCPClient
from functions.io_texts import comm_text
from functions.mode import Mode


class ModbusMode:
    def __init__(self):
        self.out_data = None
        self.client = None
        self.port = None
        self.ip = None
        init(autoreset=True)
        self.mbm = Mode()

    def params(self):
        self.ip = self.mbm.get_ip(comm_text['mb_text_1'], comm_text['mb_error_1'])
        self.port = self.mbm.get_digit(comm_text['mb_text_2'], comm_text['mb_error_2'], 1, 65535)

    def create_client(self):
        self.client = TCPClient(self.ip, int(self.port))
        if self.client.connection():
            return True
        else:
            return False


    def read(self):
        register = self.mbm.get_digit(comm_text['mb_text_3'], comm_text['mb_error_3'], 1, 65535)
        quantity = self.mbm.get_digit(comm_text['mb_text_4'], comm_text['mb_error_4'], 1, 125)
        type = self.mbm.get_enum(comm_text['mb_text_5'], comm_text['mb_error_5'], ['1', '2', '3', '4'])
        print(register, '  ', quantity, '  ', type)
        self.out_data = self.client.read(int(register), int(quantity), type)

        self.client.disconnect()
        data_len = len(self.out_data.get("reg_address"))
        if data_len > 0:
            i = -1
            while i < (data_len - 1):
                i += 1
                print(
                    Fore.LIGHTCYAN_EX + f'address: {self.out_data.get("reg_address")[i]} | int: {self.out_data.get("int")[i]}'
                                        f' | float: {self.out_data.get("float")[i][0]}' f' | bool: {self.out_data.get("bool")[i]} |'
                                        f' uint: {self.out_data.get("uint")[i]}')
        return self.out_data
