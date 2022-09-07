import argparse


class ArgParse:
    def __init__(self):
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-m", "--modbus", help="modbusTCP", action="store_true")
        self.parser.add_argument("-b", "--bacnet", help="bacnet", action="store_true")

    def args_result(self):
        args = self.parser.parse_args()
        return args
