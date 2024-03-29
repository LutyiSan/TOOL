from easymodbus import modbusClient
from loguru import logger
from colorama import Fore, init


class TCPClient:
    def __init__(self, ip_address, tcp_port):
        init(autoreset=False)

        self.tester = modbusClient.ModbusClient(str(ip_address), int(tcp_port))
        self.tester.timeout = 3.0
        self.tester.debug = True

    def connect(self):
        try:
            self.tester.connect()
            print("Modbus READY connected")
            return True
        except Exception as e:
            print("FAIL connecting", e)

    #  @func_set_timeout(5)
    def read_hr(self, reg_address, quantity):

        try:

            result = self.tester.read_holdingregisters(reg_address, quantity)

            if isinstance(result, list) and len(result) == quantity:
                return result
            else:
                return False
        except Exception as e:
            logger.exception(Fore.LIGHTRED_EX + "FAIL Read registers", e)
            return False

    #  @func_set_timeout(5)
    def read_ir(self, reg_address, quantity):
        try:
            result = self.tester.read_inputregisters(reg_address, quantity)
            if isinstance(result, list) and len(result) == quantity:
                return result
            else:
                return False
        except Exception as e:
            print(Fore.LIGHTRED_EX + "FAIL Read registers", e)
            return False

    # @func_set_timeout(5)
    def read_coils(self, reg_address, quantity):
        try:
            result = self.tester.read_coils(reg_address, quantity)
            if isinstance(result, list) and len(result) == quantity:
                return result
            else:
                return False
        except Exception as e:
            print(Fore.LIGHTRED_EX + "FAIL Read registers", e)
            return False

    #  @func_set_timeout(5)
    def read_di(self, reg_address, quantity):
        try:
            result = self.tester.read_discreteinputs(reg_address, quantity)
            if isinstance(result, list) and len(result) == quantity:
                return result
            else:
                return False
        except Exception as e:
            print(Fore.LIGHTRED_EX + "FAIL Read registers", e)
            return False

    def read(self, reg_address, quantity, reg_type):
        if self.connect():
            result = None
            if reg_type == '3':
                try:
                    result = self.read_hr(reg_address, quantity)
                except Exception as e:
                    print(Fore.LIGHTRED_EX + "READ TIMEOUT", e)
            elif reg_type == '4':
                try:
                    result = self.read_ir(reg_address, quantity)
                except Exception as e:
                    print(Fore.LIGHTRED_EX + "READ TIMEOUT", e)
            elif reg_type == '2':
                try:
                    result = self.read_di(reg_address, quantity)
                except Exception as e:
                    print(Fore.LIGHTRED_EX + "READ TIMEOUT", e)
            elif reg_type == '1':
                try:
                    result = self.read_coils(reg_address, quantity)
                except Exception as e:
                    print(Fore.LIGHTRED_EX + "READ TIMEOUT", e)
            self.disconnect()
            return result

    def disconnect(self):
        try:
            self.tester.close()
            print(Fore.LIGHTGREEN_EX + "Connection closed")
        except Exception as e:
            print(Fore.LIGHTRED_EX + "FAIL close connection", e)
