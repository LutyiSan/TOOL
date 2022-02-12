def data_to_bin_16(data):
    data_bin = bin(data)
    data_split = data_bin.split('b')[1]
    if len(data_split) < 16:
        while len(data_split) < 16:
            data_split = '0' + data_split
    return data_split


def data_to_bin_32(data):
    data_bin = bin(data)
    data_split = data_bin.split('b')[1]
    if len(data_split) < 32:
        while len(data_split) < 32:
            data_split = '0' + data_split
    return data_split


def to_int_16(data):
    if data[0] == '0':
        res = int(data, 2)
    else:
        format_data = data[1:]
        number = int(format_data, 2)
        res = 32768 - number
        res = -res
    return res


def to_int_32(data):
    if data[0] == '0':
        res = int(data, 2)
    else:
        format_data = data[1:]
        number = int(format_data, 2)
        res = 2147483648 - number
        res = -res
    return res

