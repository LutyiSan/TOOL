import pandas as pd


def append_list(cur_list, file, key):
    row = -1
    for i in cur_list:
        row += 1
        file.loc[row, key] = i


def write_scan_data(my_list, file_name):
    file = pd.DataFrame({"IP": [], "MAC_ADDRESS": [], "VENDOR": [], "STATUS": []})
    ip_list = my_list
    append_list(ip_list[0], file, 'IP')
    append_list(ip_list[1], file, 'MAC_ADDRESS')
    append_list(ip_list[2], file, 'VENDOR')
    append_list(ip_list[3], file, 'STATUS')
    file.to_excel(file_name)


def write_modbus_data(my_list, file_name):
    file = pd.DataFrame({"ADDRESS": [], "INT_VALUE": [], "FLOAT_VALUE": [], "BOOL_VALUE": [], "UINT_VALUE": []})
    data_len = len(my_list.get("reg_address"))
    i = -1
    while i < (data_len - 1):
        i += 1
        file.loc[i, 'ADDRESS'] = my_list.get("reg_address")[i]
        file.loc[i, 'INT_VALUE'] = my_list.get("int")[i][0]
        file.loc[i, 'FLOAT_VALUE'] = my_list.get("float")[i][0]
        file.loc[i, 'BOOL_VALUE'] = my_list.get("bool")[i]
        file.loc[i, 'UINT_VALUE'] = my_list.get("uint")[i]
    file.to_excel(file_name)


def write_bacnet_i_am(my_list, file_name):
    file = pd.DataFrame({"DEVICE_IP": [], "DEVICE_ID": [], "DEVICE_NAME": [], "VENDOR": []})
    data_len = len(my_list.get("DEVICE_IP"))
    i = -1
    while i < (data_len - 1):
        i += 1
        file.loc[i, 'DEVICE_IP'] = my_list.get("DEVICE_IP")[i]
        file.loc[i, 'DEVICE_ID'] = my_list.get("DEVICE_ID")[i]
        file.loc[i, 'DEVICE_NAME'] = my_list.get("DEVICE_NAME")[i]
        file.loc[i, 'VENDOR'] = my_list.get("VENDOR")[i]
    file.to_excel(f'{file_name}')


def write_bacnet_objects(my_list, file_name):
    file = pd.DataFrame({"DEVICE_IP": [], "DEVICE_ID": [], "OBJECT_TYPE": [], "OBJECT_ID": [], "OBJECT_NAME": [],
                         "DESCRIPTION": []})
    data_len = len(my_list.get("DEVICE_IP"))
    i = -1
    while i < (data_len - 1):
        i += 1
        file.loc[i, 'DEVICE_IP'] = my_list.get("DEVICE_IP")[i]
        file.loc[i, 'DEVICE_ID'] = my_list.get("DEVICE_ID")[i]
        file.loc[i, 'OBJECT_TYPE'] = my_list.get("OBJECT_TYPE")[i]
        file.loc[i, 'OBJECT_ID'] = my_list.get("OBJECT_ID")[i]
        file.loc[i, 'OBJECT_NAME'] = my_list.get("OBJECT_NAME")[i]
        file.loc[i, 'DESCRIPTION'] = my_list.get("DESCRIPTION")[i]
    file.to_excel(f'{file_name}')
