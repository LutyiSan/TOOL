from functions.scanner import Scanner
from functions.io_texts import comm_text
from functions.mode import Mode


def scan_mode():
    sm = Mode()
    ip = sm.get_ip(comm_text['scan_text_1'], comm_text['scan_error_1'])
    request = sm.get_digit(comm_text['scan_text_2'], comm_text['scan_error_2'], 1, 254)
    scanner = Scanner()
    scan_data_list = scanner.scan_hosts(ip, int(request))
    return scan_data_list
