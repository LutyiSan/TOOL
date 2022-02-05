from pythonping import ping
from getmac import get_mac_address
import sys
from colorama import init, Fore
from functions.macdetails import *


class Scanner:
    def __init__(self):
        init(autoreset=True)
        self.current_vendor = None
        self.ping_result = None
        self.current_ip = None
        self.ip_mac = None
        self.result_list = None
        self.pandas_list = [[], [], [], []]

    def scan_hosts(self, start_ip, count):
        self.result_list = []
        i = -1
        print(Fore.LIGHTBLUE_EX + f'\nStart scanning network.....')
        while i < count:
            i += 1
            a = start_ip.split(".")
            b = int(a[3]) + i
            a[3] = str(b)
            self.current_ip = ".".join(a)
            self.ping_result = ping(self.current_ip, out=sys.stdout, timeout=1, size=40, count=2, verbose=False)
            if self.ping_result.success():
                self.ip_mac = get_mac_address(ip=self.current_ip)
                self.current_vendor = get_vendor_name(self.ip_mac)
                print(Fore.LIGHTGREEN_EX + f'AVAILABLE  HOST: {self.current_ip}'
                                           f'  MAC: {self.ip_mac}  Vendor: {self.current_vendor}')
                self.result_list.append(
                    f'AVAILABLE   HOST: {self.current_ip}  MAC: {self.ip_mac}  Vendor: {self.current_vendor}')
                self.pandas_list[0].append(self.current_ip)
                self.pandas_list[1].append(self.ip_mac)
                self.pandas_list[2].append(self.current_vendor)
                self.pandas_list[3].append("Ok")
            else:

                print(Fore.LIGHTRED_EX + f'HOST {self.current_ip} UNREACHABLE')
                self.result_list.append(f'HOST {self.current_ip} UNREACHABLE')
                self.pandas_list[0].append(self.current_ip)
                self.pandas_list[1].append("UNKNOWN")
                self.pandas_list[2].append("UNKNOWN")
                self.pandas_list[3].append("Fail")

        return self.pandas_list
