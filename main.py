from colorama import init, Fore
from functions.argparser import RunMode
from functions.scan_mode import scan_mode
from functions.modbus_mode import ModbusMode
from functions.bacnet_mode import BACnetMode
from functions.write_excel import write_scan_data, write_modbus_data, write_bacnet_i_am, write_bacnet_objects


def run():
    if mode.scan:
        print(Fore.LIGHTBLUE_EX + f'#############################\n'
                                  f'#         LAN Scanner       #\n'
                                  f'#       ip, mac, vendor     #\n'
                                  f'#                           #\n'
                                  f'#############################')
        while True:
            data_list = scan_mode()
            write_scan_data(data_list, 'result_excel/_netscan.xlsx')
            print(Fore.LIGHTYELLOW_EX + f' Result write in file - result_excel/_netscan.xlsx.\n'
                                        f'Rename it and save, if you need.\nHave a nice day)!')
    elif mode.modbus:
        print(Fore.LIGHTBLUE_EX + f'#############################\n'
                                  f'#        Modbus Tester      #\n'
                                  f'#   0x01, 0x02, 0x03, 0x04  #\n'
                                  f'#                           #\n'
                                  f'#############################')
        mm = ModbusMode()
        while True:
            data_dict = None
            mm.params()
            if mm.create_client():
                while True:
                    try:
                        data_dict = mm.read()
                    except Exception as e:
                        print('TIMEOUT\n', e)
                    write_modbus_data(data_dict, 'result_excel/_modbus.xlsx')
                    print(Fore.LIGHTYELLOW_EX + f'Result write in file - result_excel/_modbus.xlsx.\n'
                                                f'Rename it and save, if you need\nHave a nice day)!')
                    change = input(Fore.LIGHTBLUE_EX + "Do you want change DEVICE(yes/no)?: ")
                    if change in ['Y', 'y', 'yes']:
                        break
                    else:
                        mm.create_client()

    elif mode.bacnet:
        print(Fore.LIGHTBLUE_EX + f'#############################\n'
                                  f'#                           #\n'
                                  f'#         BACnet Tool       #\n'
                                  f'#                           #\n'
                                  f'#############################')
        bm = BACnetMode()
        while True:
            bm.params()

            while True:
                if bm.create_client():
                    method_dict = bm.run()
                    if method_dict[0] == '1':
                        write_bacnet_i_am(method_dict[1], 'result_excel/_i_am_bacnet.xlsx')
                        print(Fore.LIGHTYELLOW_EX + f' Result write in file - result_excel/_i_am_bacnet.xlsx.\n'
                                                    f'Rename it and save, if you need.\nHave a nice day)!')
                    elif method_dict[0] == '2':
                        write_bacnet_objects(method_dict[1], 'result_excel/_object_bacnet.xlsx')
                        print(Fore.LIGHTYELLOW_EX + f' Result write in file - result_excel/_object_bacnet.xlsx.\n'
                                                    f'Rename it and save, if you need.\nHave a nice day)!')
                    change = input(Fore.LIGHTBLUE_EX + "Do you want change interface settings(yes/no)?: ")
                    if change in ['Y', 'y', 'yes']:
                        break
    else:
        print(Fore.LIGHTMAGENTA_EX + "Usage python3 main.py --help")


if __name__ == '__main__':
    init(autoreset=False)
    run_mode = RunMode()
    mode = run_mode.args_result()
    run()
