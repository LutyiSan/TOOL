class Converter:

    def __init__(self):
        self.int_32 = None
        self.int_16 = None
        self.bin_32 = None
        self.bin_16 = None

    def data_to_bin_16(self, data):
        data_bin = bin(data)
        data_split = data_bin.split('b')[1]
        if len(data_split) < 16:
            while len(data_split) < 16:
                self.bin_16 = '0' + data_split
        return self.bin_16

    def data_to_bin_32(self, data):
        data_bin = bin(data)
        data_split = data_bin.split('b')[1]
        if len(data_split) < 32:
            while len(data_split) < 32:
                self.bin_32 = '0' + data_split
        return self.bin_32

    def data_to_bin_32_word_inverse(self):
        pass

    def data_to_bin_16_byte_inverse(self):
        pass

    def data_to_bin_32_byte_inverse(self):
        pass

    def to_int_16(self, data):
        if data[0] == '0':
            self.int_16 = int(data, 2)
        else:
            format_data = data[1:]
            number = int(format_data, 2)
            self.int_16 = -32768 + number
        return self.int_16

    def to_int_32(self, data):
        if data[0] == '0':
            self.int_32 = int(data, 2)
        else:
            format_data = data[1:]
            number = int(format_data, 2)
            self.int_32 = -2147483648 + number
        return self.int_32

    def register_to_bool(self, data):
        if data != 0:
            return True
        else:
            return False

    def bit_to_bool(self, data, bit_number):
        if data[bit_number] != 0:
            return True
        else:
            return False
