from easymodbus import modbusClient
from easymodbus.modbusClient import convert_registers_to_float
from colorama import Fore
import struct
from func_timeout import func_set_timeout

def to_16bit_array(value):
    bin_value = bin(value[0])[2:]
    if len(bin_value) != 16:
        zero_array = ""
        count = 16 - len(bin_value)
        i = 0
        while i < count:
            i += 1
            zero_array += '0'
        zero_array += bin_value
        return zero_array
    else:
        return bin_value


def to_bool(value, bit_number=99):
    if bit_number == 99:
        if value != 0:
            return 'true'
        else:
            return 'false'
    elif 16 > bit_number >= 0:
        bin_value = to_16bit_array(value)[bit_number]
        if bin_value == '0':
            return 'false'
        else:
            return 'true'


def to_uint_16(value):
    if value[0] >= 0:
        return value
    else:
        return abs(value) + 32768


def to_float_32(registers):
    """
    Convert 32 Bit real Value to two 16 Bit Value to send as Modbus Registers
    floatValue: Value to be converted
    return: 16 Bit Register values int[]
    """
    b = bytearray(4)
    b[0] = registers[0] & 0xff
    b[1] = (registers[0] & 0xff00) >> 8
    b[2] = (registers[1] & 0xff)
    b[3] = (registers[1] & 0xff00) >> 8
    returnValue = struct.unpack('<f', b)  # little Endian
    return returnValue


def to_32bit_value(values):
    """
    Convert two 16 Bit Registers to 32 Bit long value - Used to receive 32 Bit values from Modbus (Modbus Registers are 16 Bit long)
    registers: 16 Bit Registers
    return: 32 bit value
    """
    return_value = (int(values[0]) & 0x0000FFFF) | (int((values[1]) << 16) & 0xFFFF0000)
    return return_value


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

    def read(self,reg_address, quantity, reg_type):
        self.result_dict = {"reg_address": [], 'int': [], 'float': [], 'bool': [], 'uint': []}
        self.reg_address = reg_address
        self.quantity = quantity
        self.reg_type = reg_type
        if self.reg_type == '3':
            self.read_hr()
        elif self.reg_type == '4':
            self.read_ir()
        elif self.reg_type == '2':
            self.read_di()
        elif self.reg_type == '1':
            self.read_coils()
        return self.result_dict

    def disconnect(self):
        try:
            self.tester.close()
            print(Fore.LIGHTGREEN_EX + "Connection closed")
        except Exception as e:
            print(Fore.LIGHTRED_EX + "Can't close connection", e)
