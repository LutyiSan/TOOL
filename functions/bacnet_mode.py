from functions.bacnet import BACnet
from functions.mode import Mode
from functions.io_texts import comm_text


class BACnetMode:
    def __init__(self):
        self.object_id = None
        self.object_type = None
        self.device_ip = None
        self.object_dict = None
        self.i_am_dict = None
        self.method = None
        self.client = None
        self.port = None
        self.ip = None
        self.mode = None

    def create_client(self):
        self.mode = Mode()
        self.ip = self.mode.get_ip(comm_text['bn_text_1'], comm_text['bn_error_1'])
        self.port = self.mode.get_digit(comm_text['bn_text_3'], comm_text['bn_error_3'], 1, 65535)
        self.client = BACnet(host_ip=self.ip, listen_port=int(self.port))
        if self.client.create_client():
            return True
        else:
            return False

    def run(self):
        self.method = self.mode.get_enum(comm_text['bn_text_5'], comm_text['bn_error_5'], ['1', '2', '3'])
        if self.method == "1":
            self.i_am_dict = self.client.who_is()
        elif self.method == "2":
            self.device_ip = self.mode.get_ip(comm_text['bn_text_2'], comm_text['bn_error_2'])
            self.object_id = self.mode.get_digit(comm_text['bn_text_4'], comm_text['bn_error_4'], 0, 4194303)
            self.object_dict = self.client.get_object_list(self.device_ip, int(self.object_id))
        elif self.method == "3":
            self.device_ip = self.mode.get_ip(comm_text['bn_text_2'], comm_text['bn_error_2'])
            self.object_type = self.mode.get_enum(comm_text['bn_text_6'], comm_text['bn_error_6'],
                                                  ['0', '1', '2', '3',
                                                   '4', '5', '13',
                                                   '14', '19'])
            self.object_id = self.mode.get_digit(comm_text['bn_text_4'], comm_text['bn_error_4'], 0, 4194303)
            self.client.read_single(self.device_ip, self.object_type, self.object_id)
        if self.method == '1':
            return self.method, self.i_am_dict
        elif self.method == '2':
            return self.method, self.object_dict
