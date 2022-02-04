from functions.bacnet import BACnet
from functions.mode import Mode
from functions.io_texts import comm_text


def bacnet_mode():
    i_am_dict = None
    object_dict = None
    bacnet_method = None
    while True:
        bacnet_mode = Mode()
        ip = bacnet_mode.get_ip(comm_text['bn_text_1'], comm_text['bn_error_1'])
        port = bacnet_mode.get_digit(comm_text['bn_text_3'], comm_text['bn_error_3'], 1, 65535)
        bacnet_client = BACnet(host_ip=ip, listen_port=int(port))
        if bacnet_client.create_client():
            bacnet_method = bacnet_mode.get_enum(comm_text['bn_text_5'], comm_text['bn_error_5'], ['1', '2', '3'])
            if bacnet_method == "1":
                i_am_dict = bacnet_client.who_is()
            elif bacnet_method == "2":
                device_ip = bacnet_mode.get_ip(comm_text['bn_text_2'], comm_text['bn_error_2'])
                object_id = bacnet_mode.get_digit(comm_text['bn_text_4'], comm_text['bn_error_4'], 0, 4194303)
                object_dict = bacnet_client.get_object_list(device_ip, int(object_id))
            elif bacnet_method == "3":
                device_ip = bacnet_mode.get_ip(comm_text['bn_text_2'], comm_text['bn_error_2'])
                object_type = bacnet_mode.get_enum(comm_text['bn_text_6'], comm_text['bn_error_6'], ['0', '1', '2', '3',
                                                                                                     '4', '5', '13',
                                                                                                     '14', '19'])
                object_id = bacnet_mode.get_digit(comm_text['bn_text_4'], comm_text['bn_error_4'], 0, 4194303)
                bacnet_client.read_single(device_ip, object_type, object_id)
        if bacnet_method == '1':
            return bacnet_method, i_am_dict
        elif bacnet_method == '2':
            return bacnet_method, object_dict
