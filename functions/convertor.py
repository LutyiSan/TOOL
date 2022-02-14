import struct

# input dict {'data': [], 'length': int, 'word_order': str, 'byte_order': str, 'type': str, 'bit_number': int}

class Converter:

    def __init__(self):
        self.float = int
        self.uint_32 = int
        self.uint_16 = int
        self.result = int
        self.int_32 = int
        self.int_16 = int
        self.bin_32 = str
        self.bin_16 = str
        self.bool = bool
        self.bit = bool

    def __data_to_bin_16(self, data):
        if isinstance(data, int):
            if data in range(0, 65535):
                data_bin = bin(data)
                data_split = data_bin.split('b')[1]
                self.bin_16 = data_split
                if len(self.bin_16) < 16:
                    while len(self.bin_16) < 16:
                        self.bin_16 = '0' + self.bin_16
                else:
                    self.bin_16 = data_split
                return self.bin_16
            else:
                raise Exception("Value Error | Data is out of range (0, 65535)")
        else:
            raise Exception("Type Error | Data is not Digit")

    def __data_to_bin_32(self, data):
        first_word = ""
        second_word = ""
        if isinstance(data, list) and len(data) == 2:
            if data[0] in range(0, 65535) and data[1] in range(0, 65535):
                data1_bin = bin(data[0])
                data2_bin = bin(data[1])
                data1_split = data1_bin.split('b')[1]
                data2_split = data2_bin.split('b')[1]
                if len(data1_split) < 16:
                    while len(first_word) < 16:
                        data1_split = '0' + data1_split
                        first_word = data1_split
                else:
                    first_word = data1_split
                if len(data2_split) < 16:
                    while len(second_word) < 16:
                        data2_split = '0' + data2_split
                        second_word = data2_split
                else:
                    second_word = data2_split

                self.bin_32 = first_word + second_word
                return self.bin_32
            else:
                raise Exception("Value Error | Data[0] or Data[1] is out of range (0, 255)")
        else:
            raise Exception("Type Error | Data is not str or length Data != 32")

    def __data_to_bin_32_word_inverse(self):
        if isinstance(self.bin_32, str) and len(self.bin_32) == 32:
            first_word = self.bin_32[16:]
            second_word = self.bin_32[:16]
            self.bin_32 = first_word + second_word
            return self.bin_32
        else:
            raise Exception('Input Data is not a string or length != 32')

    def __data_to_bin_16_byte_inverse(self):
        if isinstance(self.bin_16, str) and len(self.bin_16) == 16:
            first_byte = self.bin_16[8:]
            second_byte = self.bin_16[:8]
            self.bin_16 = first_byte + second_byte
            return self.bin_16
        else:
            raise Exception('Input Data is not a string or length != 16')

    def __data_to_bin_32_byte_inverse(self):
        if isinstance(self.bin_32, str) and len(self.bin_32) == 32:
            first_byte = self.bin_32[8:16]
            second_byte = self.bin_32[:8]
            third_byte = self.bin_32[24:]
            fourth_byte = self.bin_32[16:24]
            self.bin_32 = first_byte + second_byte + third_byte + fourth_byte
            return self.bin_32
        else:
            raise Exception('Input Data is not a string or length != 32')

    def __to_int_16(self):
        if isinstance(self.bin_16, str) and len(self.bin_16) == 16:
            if self.bin_16[0] == '0':
                self.int_16 = int(self.bin_16, 2)
            else:
                format_data = self.bin_16[1:]
                number = int(format_data, 2)
                self.int_16 = -32768 + number
            return self.int_16
        else:
            raise Exception('Input Data is not a string or length != 16')

    def __to_int_32(self):
        if isinstance(self.bin_32, str) and len(self.bin_32) == 32:
            if self.bin_32[0] == '0':
                self.int_32 = int(self.bin_32, 2)
            else:
                format_data = self.bin_32[1:]
                number = int(format_data, 2)
                self.int_32 = -2147483648 + number
            return self.int_32
        else:
            raise Exception('Input Data is not a string or length != 32')

    def __to_uint_16(self):
        if isinstance(self.bin_16, str) and len(self.bin_16) == 16:
            self.uint_16 = int(self.bin_16, 2)
            return self.uint_16
        else:
            raise Exception('Input Data is not str or string length != 16')

    def __to_uint_32(self, data, word_inverse, byte_inverse):

        if isinstance(data, list):
            if len(data) == 2:
                if not word_inverse and not byte_inverse:
                    if data[0] in range(0, 65535) and data[1] in range(0, 65535):
                        self.uint_32 = (int(data[0]) & 0x0000FFFF) | (int((data[1]) << 16) & 0xFFFF0000)
                        return self.uint_32
                elif word_inverse and not byte_inverse:
                    if data[0] in range(0, 65535) and data[1] in range(0, 65535):
                        self.uint_32 = (int(data[1]) & 0x0000FFFF) | (int((data[0]) << 16) & 0xFFFF0000)
                        return self.uint_32
                elif not word_inverse and byte_inverse:
                    first = int(self.bin_32[:16], 2)
                    second = int(self.bin_32[16:], 2)
                    self.uint_32 = (int(first) & 0x0000FFFF) | (int((second) << 16) & 0xFFFF0000)
                    return self.uint_32
                elif word_inverse and byte_inverse:
                    first = int(self.bin_32[:16], 2)
                    second = int(self.bin_32[16:], 2)
                    self.uint_32 = (int(first) & 0x0000FFFF) | (int((second) << 16) & 0xFFFF0000)
                    return self.uint_32
            else:
                raise Exception('Length Data != 2')
        else:
            raise Exception('Input Data is not a list()')

    def __to_float(self, data, word_inverse, byte_inverse):

        if isinstance(data, list) and len(data) == 2:
            if data[0] in range(0, 65535) and data[1] in range(0, 65535):
                if not byte_inverse:
                    b = bytearray(4)
                    b[0] = data[0] & 0xff
                    b[1] = (data[0] & 0xff00) >> 8
                    b[2] = (data[1] & 0xff)
                    b[3] = (data[1] & 0xff00) >> 8
                    if not word_inverse:
                        self.float = struct.unpack('<f', b)  # little Endian
                        return self.float
                    elif word_inverse:
                        self.float = struct.unpack('>f', b)  # big Endian
                        return self.float
                elif byte_inverse:
                    print(self.bin_32)

                    first = int(self.bin_32[:16], 2)
                    second = int(self.bin_32[16:], 2)
                    print(first)
                    print(second)
                    b = bytearray(4)
                    b[0] = first & 0xff
                    b[1] = (first & 0xff00) >> 8
                    b[2] = (second & 0xff)
                    b[3] = (second & 0xff00) >> 8
                    if not word_inverse:
                        self.float = struct.unpack('<f', b)  # little Endian
                        return self.float
                    elif word_inverse:
                        self.float = struct.unpack('>f', b)  # big Endian
                        return self.float
            else:
                raise Exception('Data[0] or Data[1] out of range (0,255)')
        else:
            raise Exception('Input Data is not a list() or data length !=2')

    def __register_to_bool(self):
        if isinstance(self.bin_16, str) and len(self.bin_16) == 16:
            data = int(self.bin_16, 2)
            if data != 0:
                self.bool = True
                return self.bool
            else:
                self.bool = False
                return self.bool
        else:
            raise Exception('Input Data is not a string or data length !=16')

    def __bit_to_bool(self, bit_number):
        if isinstance(self.bin_16, str) and len(self.bin_16) == 16:
            if isinstance(bit_number, int) and bit_number in range(0, 15):
                if int(self.bin_16[bit_number]) != 0:
                    self.bit = True
                    return self.bit
                else:
                    self.bit = False
                    return self.bit
            else:
                raise Exception('Bit number is out of range (0-15')
        else:
            raise Exception('Input Data is not a string or data length !=16')

    def convert_16_bit_big_big(self, params):
        self.__data_to_bin_16(params['data'][0])
        if params['type'] == 'int_16':
            self.result = self.__to_int_16()
        elif params['type'] == 'uint_16':
            self.result = self.__to_uint_16()
        elif params['type'] == 'bool':
            self.result = self.__register_to_bool()
        elif params['type'] == 'bit':
            self.result = self.__bit_to_bool(params['bit_number'])

    def convert_16_bit_big_little(self, params):
        self.__data_to_bin_16_byte_inverse()
        if params['type'] == 'int_16':
            self.result = self.__to_int_16()
        elif params['type'] == 'uint_16':
            self.result = self.__to_uint_16()
        elif params['type'] == 'bool':
            self.result = self.__register_to_bool()
        elif params['type'] == 'bit':
            self.result = self.__bit_to_bool(params['bit_number'])

    def convert_32_bit_big_big(self, params):
        if params['type'] == 'int_32':
            self.result = self.__to_int_32()
        elif params['type'] == 'uint_32':
            self.result = self.__to_uint_32(params['data'], False, False)
        elif params['type'] == 'float':
            self.result = self.__to_float(params['data'], False, False)

    def convert_32_bit_little_big(self, params):
        self.__data_to_bin_32_word_inverse()
        if params['type'] == 'int_32':
            self.result = self.__to_int_32()
        elif params['type'] == 'uint_32':
            self.result = self.__to_uint_32(params['data'], True, False)
        elif params['type'] == 'float':
            self.result = self.__to_float(params['data'], True, False)

    def convert_32_bit_big_little(self, params):
        self.__data_to_bin_32_byte_inverse()
        if params['type'] == 'int_32':
            self.result = self.__to_int_32()
        elif params['type'] == 'uint_32':
            self.result = self.__to_uint_32(params['data'], False, True)
        elif params['type'] == 'float':
            self.result = self.__to_float(params['data'], False, True)

    def convert_32_bit_little_little(self, params):
        self.__data_to_bin_32_word_inverse()
        self.__data_to_bin_32_byte_inverse()
        if params['type'] == 'int_32':
            self.result = self.__to_int_32()
        elif params['type'] == 'uint_32':
            self.result = self.__to_uint_32(params['data'], True, True)
        elif params['type'] == 'float':
            self.result = self.__to_float(params['data'], True, True)

    def convert(self, params):
        if params['length'] == 16:
            self.__data_to_bin_16(params['data'][0])
            if params['byte_order'] == 'big':
                self.convert_16_bit_big_big(params)
            elif params['byte_order'] == 'little':
                self.convert_16_bit_big_little(params)
        if params['length'] == 32:
            self.__data_to_bin_32(params['data'])
            if params['word_order'] == 'big' and params['byte_order'] == 'big':
                self.convert_32_bit_big_big(params)
            elif params['word_order'] == 'little' and params['byte_order'] == 'big':
                self.convert_32_bit_little_big(params)
            elif params['word_order'] == 'big' and params['byte_order'] == 'little':
                self.convert_32_bit_big_little(params)
            elif params['word_order'] == 'little' and params['byte_order'] == 'little':
                self.convert_32_bit_little_little(params)
        print(self.result)
        return self.result
