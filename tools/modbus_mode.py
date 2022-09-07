from colorama import Fore, init
from tools.modbustcp import TCPClient
from tools.validator import *


class ModbusMode:
    init(autoreset=True)

    def device_params(self):
        ip_state = False
        port_state = False
        while not ip_state:
            self.ip = input(Fore.LIGHTYELLOW_EX + "input device ip-address:  ")
            if validate_ip(self.ip):
                ip_state = True
            else:
                print(Fore.LIGHTRED_EX + "WRONG ip-address!")
        while not port_state:
            self.port = input(Fore.LIGHTYELLOW_EX + "input device tcp-port:  ")
            if validate_digit(self.port, 1, 65535):
                port_state = True
            else:
                print(Fore.LIGHTRED_EX + "WRONG port number!")

    def create_client(self):

        self.client = TCPClient(self.ip, self.port)
      #  self.client.connect()


    def read_params(self):
        reg_state = False
        quanty_state = False
        type_state = False
        while not reg_state:
            self.registers = input(Fore.LIGHTYELLOW_EX + "input registers address (0-65535):  ")
            if validate_digit(self.registers, 0, 65535):
                reg_state = True
            else:
                print(Fore.LIGHTRED_EX + "WRONG registers address!")
        while not quanty_state:
            self.quantity = input(Fore.LIGHTYELLOW_EX + "input read quantity (1-125):  ")
            if validate_digit(self.quantity, 1, 125):
                quanty_state = True
            else:
                print(Fore.LIGHTRED_EX + "WRONG quantity!")
        while not type_state:
            self.reg_type = input(Fore.LIGHTYELLOW_EX + "input registers type 1=COIL 2=DISCRETE 3=HOLDING 4=INPUT:  ")
            if validate_in_enum(['1', '2', '3', '4'], self.reg_type):
                type_state = True
            else:
                print(Fore.LIGHTRED_EX + "WRONG registers type!")

    def read_registers(self):
        read_data = self.client.read(int(self.registers), int(self.quantity), self.reg_type)
        if isinstance(read_data, list):
            count = -1
            for i in read_data:
                count += 1
                print(Fore.LIGHTCYAN_EX + f'register {int(self.registers) + count} value: {i}')
        else:
            print(Fore.LIGHTRED_EX + "FAIL read!")


