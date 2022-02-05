from colorama import init, Fore
from functions.argparser import RunMode
from functions.scan_mode import scan_mode
from functions.modbus_mode import modbus_mode
from functions.bacnet_mode import bacnet_mode
#from functions.write_excel import write_scan_data, write_modbus_data, write_bacnet_i_am, write_bacnet_objects


def run():
    if mode.scan:
        print(Fore.LIGHTBLUE_EX + f'#############################\n'
                                  f'#         LAN Scanner       #\n'
                                  f'#       ip, mac, vendor     #\n'
                                  f'#                           #\n'
                                  f'#############################')
        data_list = scan_mode()
     #   write_scan_data(data_list, 'result_excel/_netscan.xlsx')
        print(Fore.LIGHTYELLOW_EX + f' Result write in file - result_excel/_netscan.xlsx\n'
                                    f'rename it and save if you need\nHave a nice day)!')
    elif mode.modbus:
        print(Fore.LIGHTBLUE_EX + f'#############################\n'
                                  f'#        Modbus tester      #\n'
                                  f'#   0x01, 0x02, 0x03, 0x04  #\n'
                                  f'#                           #\n'
                                  f'#############################')
        data_dict = modbus_mode()
        if data_dict is not None:
    #        write_modbus_data(data_dict, 'result_excel/_modbus.xlsx')
            print(Fore.LIGHTYELLOW_EX + f'Result write in file - result_excel/_modbus.xlsx\n'
                                        f'rename it and save if you need\nHave a nice day)!')
    elif mode.bacnet:
        print(Fore.LIGHTBLUE_EX + f'#############################\n'
                                  f'#                           #\n'
                                  f'#         BACnet Tool       #\n'
                                  f'#                           #\n'
                                  f'#############################')
        bacnet_method = bacnet_mode()
        if bacnet_method[0] == '1':
    #        write_bacnet_i_am(bacnet_method[1], 'result_excel/_i_am_bacnet.xlsx')
            print(Fore.LIGHTYELLOW_EX + f' Result write in file - result_excel/_i_am_bacnet.xlsx\n'
                                        f'rename it and save if you need\nHave a nice day)!')
        elif bacnet_method[0] == '2':
    #        write_bacnet_objects(bacnet_method[1], 'result_excel/_object_bacnet.xlsx')
            print(Fore.LIGHTYELLOW_EX + f' Result write in file - result_excel/_object_bacnet.xlsx\n'
                                        f'rename it and save if you need\nHave a nice day)!')

    else:
        print(Fore.LIGHTMAGENTA_EX + "Usage python3 main.py --help")


if __name__ == '__main__':
    init(autoreset=False)
    run_mode = RunMode()
    mode = run_mode.args_result()
    run()
