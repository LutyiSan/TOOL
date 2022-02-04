import argparse


class RunMode:
    def __init__(self):
        self.args = None
        self.parser = argparse.ArgumentParser()
        self.parser.add_argument("-s", "--scan", help="net scanner", action="store_true")
        self.parser.add_argument("-m", "--modbus", help="modbusTCP", action="store_true")
        self.parser.add_argument("-b", "--bacnet", help="bacnet", action="store_true")

    def args_result(self):
        self.args = self.parser.parse_args()
        return self.args
