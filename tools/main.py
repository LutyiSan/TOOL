from colorama import init, Fore
from argparser import ArgParse

from modbus_mode import ModbusMode
from bacnet_mode import BACnetMode
from write_excel import write_bacnet_i_am, write_bacnet_objects


def run():

    if mode.modbus:
        print(Fore.LIGHTBLUE_EX + f'#############################\n'
                                  f'#        Modbus Tester      #\n'
                                  f'#   FC01, FC02, FC03, FC04  #\n'
                                  f'#                           #\n'
                                  f'#############################')
        modbus = ModbusMode()
        while True:
            read_data = None
            modbus.device_params()
            modbus.create_client()
            while True:
                modbus.read_params()
                modbus.read_registers()
                change = input(Fore.LIGHTBLUE_EX + "Do you want change DEVICE(yes/no)?: ")
                if change in ['Y', 'y', 'yes']:
                    break
                else:
                    modbus.create_client()


    elif mode.bacnet:
        print(Fore.LIGHTBLUE_EX + f'##########################################\n'
                                  f'#              BACnet Tool               #\n'
                                  f'#   who-is, object-list, read-property   #\n'
                                  f'#                                        #\n'
                                  f'##########################################')
        bacnet = BACnetMode()
        while True:
            bacnet.client_params()
            while True:
                if bacnet.create_client():
                    method_dict = bacnet.run()
                    if method_dict is not None:
                        if method_dict[0] == '1':
                            write_bacnet_i_am(method_dict[1], 'result_excel/_i_am_bacnet.csv')
                            print(Fore.LIGHTYELLOW_EX + f' Result write in file - result_excel/_i_am_bacnet.xlsx.\n'
                                                        f'Rename it and save, if you need.\nHave a nice day)!')
                        elif method_dict[0] == '2':
                            write_bacnet_objects(method_dict[1], 'result_excel/_object_bacnet.csv')
                            print(Fore.LIGHTYELLOW_EX + f' Result write in file - result_excel/_object_bacnet.xlsx.\n'
                                                        f'Rename it and save, if you need.\nHave a nice day)!')
                    change = input(Fore.LIGHTBLUE_EX + "Do you want change interface settings(yes/no)?: ")
                    if change in ['Y', 'y', 'yes']:
                        break
                else:
                    break
    else:
        print(Fore.LIGHTMAGENTA_EX + "Usage python3 main.py --help")


if __name__ == '__main__':
    init(autoreset=False)
    run_mode = ArgParse()
    mode = run_mode.args_result()
    run()
