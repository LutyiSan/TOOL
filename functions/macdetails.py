import requests


def get_mac_details(mac_address):
    url = "https://api.macvendors.com/"
    response = requests.get(url + mac_address)
    if response.status_code != 200:
        return "UNKNOWN"
    return response.content.decode()


def get_vendor_name(mac_address):
    try:
        vendor_name = get_mac_details(mac_address)
        return vendor_name
    except:
        return "UNKNOWN"
