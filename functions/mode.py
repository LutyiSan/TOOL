from functions.validator import *
from colorama import Fore
import time


class Mode:
    def __init__(self):
        self.result = []

    def get_ip(self, input_text, error_text):
        ip = None
        valid = False
        while not valid:
            ip = input(Fore.LIGHTYELLOW_EX + input_text)
            valid = validate_ip(ip)
            if valid:
                self.result.append(ip)
            else:
                print(Fore.LIGHTRED_EX + error_text)
                time.sleep(1.3)
        return ip

    def get_digit(self, input_text, error_text, start, stop):
        curr_digit = None
        valid = False
        while not valid:
            curr_digit = input(Fore.LIGHTYELLOW_EX + input_text)
            valid = validate_digit(curr_digit, start, stop)
            if valid:
                self.result.append(curr_digit)
            else:
                print(Fore.LIGHTRED_EX + error_text)
                time.sleep(1.3)
        return curr_digit

    def get_enum(self, input_text, error_text, enum):
        enum_value = None
        valid = False
        while not valid:
            enum_value = input(Fore.LIGHTYELLOW_EX + input_text)
            if enum_value in enum:
                valid = True
                self.result.append(enum_value)
            else:
                print(Fore.LIGHTRED_EX + error_text)
                time.sleep(1.3)
        return enum_value
