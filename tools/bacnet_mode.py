from tools.bacnet import BACnet
from colorama import Fore, init
from tools.validator import *


class BACnetMode:
    init(autoreset=False)

    def client_params(self):
        ip_state = False
        port_state = False
        while not ip_state:
            self.ip = input(Fore.LIGHTYELLOW_EX + "input host ip-address:  ")
            if validate_ip(self.ip):
                ip_state = True
            else:
                print(Fore.LIGHTRED_EX + "WRONG ip-address!")
        while not port_state:
            self.port = input(Fore.LIGHTYELLOW_EX + "input device udp-port:  ")
            if validate_digit(self.port, 1, 65535):
                port_state = True
            else:
                print(Fore.LIGHTRED_EX + "WRONG port number!")
        self.client = BACnet(host_ip=self.ip, listen_port=int(self.port))

    def create_client(self):
        if self.client.create_client():
            return True
        else:
            return False

    def run(self):
        method_state = False
        while not method_state:
            self.method = input(Fore.LIGHTYELLOW_EX + "Choice action 1=WHO-IS, 2=RAED OBJECT-LIST 3=READ OBJECT:  ")
            if validate_in_enum(['1', '2', '3'], self.method):
                method_state = True
            else:
                print(Fore.LIGHTRED_EX + "WRONG choice!")
        if self.method == "1":
            return self.method, self.who_is()
        elif self.method == "2":
            return self.method, self.object_list()
        elif self.method == "3":
            self.read_object()


    def who_is(self):
        i_am_dict = self.client.who_is()
        return i_am_dict

    def object_list(self):
        ip_state = False
        id_state = False
        while not ip_state:
            self.device_ip = input(Fore.LIGHTYELLOW_EX + "input device ip-address:  ")
            if validate_ip(self.device_ip):
                ip_state = True
            else:
                print(Fore.LIGHTRED_EX + "WRONG ip-address!")
        while not id_state:
            self.object_id = input(Fore.LIGHTYELLOW_EX + "input device ID:  ")
            if validate_digit(self.object_id, 1, 4194303):
                id_state = True
            else:
                print(Fore.LIGHTRED_EX + "WRONG device ID!")
        object_list = self.client.get_object_list(self.device_ip, int(self.object_id))
        return object_list

    def read_object(self):
        ip_state = False
        ot_state = False
        oid_state = False
        while not ip_state:
            self.device_ip = input(Fore.LIGHTYELLOW_EX + "input device ip-address:  ")
            if validate_ip(self.device_ip):
                ip_state = True
            else:
                print(Fore.LIGHTRED_EX + "WRONG ip-address!")
        while not ot_state:
            self.object_type = input(Fore.LIGHTYELLOW_EX + "Object type (0,1,2,3,4,5,13,14,19):  ")
            if validate_in_enum(['1', '2', '3', '4', '5', '13', '14', '19'], self.object_type):
                ot_state = True
            else:
                print(Fore.LIGHTRED_EX + "WRONG Object type!")
        while not oid_state:
            self.object_id = input(Fore.LIGHTYELLOW_EX + "input object ID:  ")
            if validate_digit(self.object_id, 1, 4194303):
                oid_state = True
            else:
                print(Fore.LIGHTRED_EX + "WRONG object ID!")
        print(self.device_ip, self.object_type, self.object_id)
        self.client.read_single(self.device_ip, self.object_type, self.object_id)

