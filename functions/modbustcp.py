from easymodbus import modbusClient
from easymodbus.modbusClient import convert_registers_to_float
from colorama import Fore
from func_timeout import func_set_timeout


def to_bool_and_uint(int_data):
    if int_data[0] == 0:
        bool_value = "FALSE"
    else:
        bool_value = "TRUE"
    output_value = bin(int_data[0])
    output_value = output_value.split("b")[1]
    if int_data[0] >= 0:
        uint_value = int_data[0]
    else:
        output_value = output_value + "0"
        uint_value = int(output_value, 2)
    return bool_value, uint_value


class TCPClient:
    def __init__(self, ip_address, tcp_port):
        self.output_value = None
        self.connect_state = None
        self.ip = ip_address
        self.port = tcp_port
        self.reg_address = None
        self.quantity = None
        self.reg_type = None
        self.tester = modbusClient.ModbusClient(self.ip, self.port)
        self.result_dict = {"reg_address": [], 'int': [], 'float': [], 'bool': [], 'uint': []}

    def connection(self):
        try:
            self.tester.connect()
            print(Fore.LIGHTGREEN_EX + "Connection Ready")
            return True
        except Exception as e:
            self.connect_state = False
            print(Fore.LIGHTRED_EX + "Can't connect to device", e)
            return False

    @func_set_timeout(5)
    def read_hr(self):
        count = -1
        while count < (self.quantity - 1):
            count += 1
            try:
                result = self.tester.read_holdingregisters(self.reg_address + count, 1)
                self.result_dict["reg_address"].append(self.reg_address + count)
                if isinstance(result, list) and len(result) != 0:
                    self.result_dict["int"].append(result[0])
                result_float = convert_registers_to_float(
                    self.tester.read_holdingregisters(self.reg_address + count, 2))
                if isinstance(result_float, tuple) and len(result) != 0:
                    self.result_dict["float"].append(result_float)
                convert_data = to_bool_and_uint(result)
                if isinstance(convert_data, tuple) and len(convert_data) != 0:
                    self.result_dict["bool"].append(convert_data[0])
                    self.result_dict["uint"].append(convert_data[1])
            except Exception as e:
                self.result_dict["int"].append("none")
                self.result_dict["float"].append("none")
                self.result_dict["bool"].append("none")
                self.result_dict["uint"].append("none")
                print(Fore.LIGHTRED_EX + "Can't Read registers", e)

    @func_set_timeout(5)
    def read_ir(self):
        count = -1
        while count < self.quantity:
            count += 1
            try:
                result = self.tester.read_inputregisters(self.reg_address + count, 1)
                self.result_dict["reg_address"].append(self.reg_address + count)
                if isinstance(result, list) and len(result) != 0:
                    self.result_dict["int"].append(result[0])
                result_float = convert_registers_to_float(
                    self.tester.read_inputregisters(self.reg_address + count, 2))

                if isinstance(result_float, tuple) and len(result) != 0:
                    self.result_dict["float"].append(result_float)
                convert_data = to_bool_and_uint(result)
                if isinstance(convert_data, tuple) and len(convert_data) == 2:
                    self.result_dict["bool"].append(convert_data[0])
                    self.result_dict["uint"].append(convert_data[1])
            except Exception as e:
                self.result_dict["int"].append("none")
                self.result_dict["float"].append("none")
                self.result_dict["bool"].append("none")
                self.result_dict["uint"].append("none")
                print(Fore.LIGHTRED_EX + "Can't Read registers", e)

    @func_set_timeout(5)
    def read_coils(self):
        count = -1
        while count < self.quantity:
            count += 1
            try:
                result = self.tester.read_coils(self.reg_address + count, 1)
                self.result_dict["reg_address"].append(self.reg_address + count)
                if isinstance(result, list) and len(result) == 1:
                    self.result_dict["int"].append("none")
                    self.result_dict["float"].append(("none",))
                    self.result_dict["bool"].append(result[0])
                    self.result_dict["uint"].append('none')
            except Exception as e:
                self.result_dict["int"].append("none")
                self.result_dict["float"].append(("none",))
                self.result_dict["bool"].append("none")
                self.result_dict["uint"].append("none")
                print(Fore.LIGHTRED_EX + "Can't Read registers", e)

    @func_set_timeout(5)
    def read_di(self):
        count = -1
        while count < self.quantity:
            count += 1
            try:
                result = self.tester.read_discreteinputs(self.reg_address + count, 1)
                self.result_dict["reg_address"].append(self.reg_address + count)
                if isinstance(result, list) and len(result) == 1:
                    self.result_dict["int"].append("none")
                    self.result_dict["float"].append(("none",))
                    self.result_dict["bool"].append(result[0])
                    self.result_dict["uint"].append('none')
            except Exception as e:
                self.result_dict["int"].append("none")
                self.result_dict["float"].append(("none",))
                self.result_dict["bool"].append("none")
                self.result_dict["uint"].append("none")
                print(Fore.LIGHTRED_EX + "Can't Read registers", e)

    def read(self, reg_address, quantity, reg_type):
        self.result_dict = {"reg_address": [], 'int': [], 'float': [], 'bool': [], 'uint': []}
        self.reg_address = reg_address
        self.quantity = quantity
        self.reg_type = reg_type
        if self.reg_type == '3':
            try:
                self.read_hr()
            except:
                print(Fore.LIGHTRED_EX + "READ TIMEOUT")
        elif self.reg_type == '4':
            try:
                self.read_ir()
            except:
                print(Fore.LIGHTRED_EX + "READ TIMEOUT")
        elif self.reg_type == '2':
            try:
                self.read_di()
            except:
                print(Fore.LIGHTRED_EX + "READ TIMEOUT")
        elif self.reg_type == '1':
            try:
                self.read_coils()
            except:
                print(Fore.LIGHTRED_EX + "READ TIMEOUT")
        return self.result_dict

    def disconnect(self):
        try:
            self.tester.close()
            print(Fore.LIGHTGREEN_EX + "Connection closed")
        except Exception as e:
            print(Fore.LIGHTRED_EX + "Can't close connection", e)
