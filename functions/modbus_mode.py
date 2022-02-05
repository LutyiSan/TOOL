from colorama import Fore, init
from functions.modbustcp import TCPClient
from functions.io_texts import comm_text
from functions.mode import Mode


def modbus_mode():
    init(autoreset=True)
    mbm = Mode()
    ip = mbm.get_ip(comm_text['mb_text_1'], comm_text['mb_error_1'])
    port = mbm.get_digit(comm_text['mb_text_2'], comm_text['mb_error_2'], 1, 65535)
    register = mbm.get_digit(comm_text['mb_text_3'], comm_text['mb_error_3'], 1, 65535)
    quantity = mbm.get_digit(comm_text['mb_text_4'], comm_text['mb_error_4'], 1, 125)
    type = mbm.get_enum(comm_text['mb_text_5'], comm_text['mb_error_5'], ['1', '2', '3', '4'])
    client = TCPClient(ip, int(port), int(register), int(quantity), type)
    if client.connection():
        out_data = client.read()
        print(out_data)
        client.disconnect()
        data_len = len(out_data.get("reg_address"))
        i = -1
        while i < (data_len - 1):
            i += 1
            print(Fore.LIGHTCYAN_EX + f'address: {out_data.get("reg_address")[i]} | int: {out_data.get("int")[i]}'
                                      f' | float: {out_data.get("float")[i][0]}' f' | bool: {out_data.get("bool")[i]} |'
                                      f' uint: {out_data.get("uint")[i]}')
        return out_data
    else:
        pass
