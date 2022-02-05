import BAC0
from colorama import Fore, init


class BACnet:
    def __init__(self, host_ip="localhost", netmask='24', listen_port=47808):
        self.desk = None
        self.name = None
        init(autoreset=True)
        self.bacnet_client = None
        self.single_point_list = list()
        self.object_dict = {"DEVICE_IP": [], 'DEVICE_ID': [], 'OBJECT_TYPE': [], 'OBJECT_ID': [], 'OBJECT_NAME': [],
                            'DESCRIPTION': []}
        self.i_am_dict = {'DEVICE_IP': [], 'DEVICE_ID': [], "DEVICE_NAME": [], 'VENDOR': []}
        self.my_interface = host_ip
        self.netmask = netmask
        self.listen_port = listen_port

    def create_client(self):
        try:
            self.bacnet_client = BAC0.lite(ip=f'{self.my_interface}/{self.netmask}', port=self.listen_port)
            print(Fore.LIGHTGREEN_EX + "BACnet Client READY")
            return True
        except Exception as e:
            print(Fore.LIGHTRED_EX + "FAIL create BACnet Client", e)
        return False

    def who_is(self):
        try:
            i_am_list = self.bacnet_client.whois()
            if len(i_am_list) > 0:
                for i in i_am_list:
                    name = self.bacnet_client.read(f'{i[0]}/{self.netmask} device {i[1]} objectName')
                    vendor = self.bacnet_client.read(f'{i[0]}/{self.netmask} device {i[1]} vendorName')
                    self.i_am_dict['DEVICE_IP'].append(i[0])
                    self.i_am_dict['DEVICE_ID'].append(i[1])
                    if isinstance(name, (str, list)) and len(name) > 0:
                        self.i_am_dict['DEVICE_NAME'].append(name)
                    else:
                        name = "unknown"
                        self.i_am_dict['DEVICE_NAME'].append('unknown')
                    if isinstance(name, (str, list)) and len(name) > 0:
                        self.i_am_dict['VENDOR'].append(vendor)
                    else:
                        vendor = "unknown"
                        self.i_am_dict['VENDOR'].append('unknown')
                    print(Fore.LIGHTGREEN_EX + f'ip: {i[0]} | id: {i[1]} | name: {name} | vendor: {vendor}')
        except Exception as e:
            print(Fore.LIGHTRED_EX + "NO RESPONSE WHO-IS", e)
        self.bacnet_client.disconnect()

        return self.i_am_dict

    def read_single(self, device_ip, object_type, object_id):
        object_types = {"0": 'analogInput', '1': 'analogOutput', '2': 'analogValue', '3': 'binaryInput',
                        '4': 'binaryOutput', '5': 'binaryValue', '13': 'multistateInput', '14': 'multistateOutput',
                        '19': 'multistateValue'}
        obj_type = object_types[f'{object_type}']
        try:
            pv = self.bacnet_client.read(f'{device_ip}/{self.netmask} {obj_type} {object_id} presentValue')
            if isinstance(pv, (str, int, float)):
                self.single_point_list.append(pv)
                sf = self.bacnet_client.read(f'{device_ip}/{self.netmask} {obj_type} {object_id} statusFlags')
                if isinstance(sf, list) and len(sf) == 4:
                    self.single_point_list.append(sf)
                else:
                    self.single_point_list.append('unknown')
                rl = self.bacnet_client.read(f'{device_ip}/{self.netmask} {obj_type} {object_id} reliability')
                if isinstance(sf, (list, str)) and len(sf) > 0:
                    self.single_point_list.append(rl)
                else:
                    self.single_point_list.append('unknown')
            else:
                self.single_point_list.append('unknown')
            print(Fore.LIGHTGREEN_EX + f'{obj_type} | {object_id} | {self.single_point_list[0]} | '
                                       f'{self.single_point_list[1]} | {self.single_point_list[2]}')
        except Exception as e:
            print(Fore.LIGHTRED_EX + "Can't read property", e)
        self.bacnet_client.disconnect()

    def get_object_list(self, device_ip, device_id):
        try:
            object_list = self.bacnet_client.read(
                f'{device_ip}/{self.netmask} device {device_id} objectList')
            objects_len = len(object_list)
            if objects_len > 0:
                for i in object_list:
                    self.name = self.bacnet_client.read(
                        f'{device_ip}/{self.netmask} {i[0]} {i[1]} objectName')
                    self.object_dict['DEVICE_IP'].append(device_ip)
                    self.object_dict['DEVICE_ID'].append(device_id)
                    self.object_dict['OBJECT_TYPE'].append(i[0])
                    self.object_dict['OBJECT_ID'].append(i[1])
                    if isinstance(self.name, (str, list)) and len(self.name) > 0:
                        self.object_dict['OBJECT_NAME'].append(self.name)
                    else:
                        self.object_dict['OBJECT_NAME'].append('unknown')
                    self.desk = self.bacnet_client.read(
                        f'{device_ip}/{self.netmask} {i[0]} {i[1]} description')
                    if isinstance(self.desk, (str, list)) and len(self.desk) > 0:
                        self.object_dict['DESCRIPTION'].append(self.desk)
                    else:
                        self.object_dict['DESCRIPTION'].append('unknown')
                    print(Fore.LIGHTGREEN_EX + f'OBJECT_TYPE: {i[0]}  OBJECT_ID: {i[1]}  NAME: {self.name}'
                                               f' DESCRIPTION: {self.desk}')
            print(f"{objects_len}  objects in device")
        except Exception as e:
            print(Fore.LIGHTRED_EX + "Can't get object-list", e)
        self.bacnet_client.disconnect()
        return self.object_dict

    def disconnect(self):
        self.bacnet_client.disconnect()
        pass
