# TOOL
This tools, which create for use into Linux OS, for DDC engineer.
1. NET-SCANNER - scan lAN and get IP, MAC:, Vendor-Name. All getting data output to terminal and write in excel-file.
2. Modbus-Tester raed data from ModbusTCP devices. All getting data output to terminal and write in excel-file.
3. BACnet-Tools. 
    3.1 Scanning BACnet usage "Who-Is". All getting data output to terminal and write in excel-file.
    3.2 Get object-list choices device. All getting data output to terminal and write in excel-file.
    3.3 read property (present-value, status-flags, reliability) of object-types( AI, AO, AV, BI, BO , BV, MSI, MSO,MSV). All getting data output to terminal and write in excel-file..

# Installations
cd /opt
git clone https://github.com/LutyiSan/TOOL
cd /TOOL
sudo sh install.sh
# Usage
cd /opt/TOOL
sudo python3 main.py --scan or -s, so you are starting  NET-SCANNER MODE
sudo python3 main.py --modbus or -m, so you are starting  MODBUS-TESTER MODE
sudo python3 main.py --bacnet or -b, so you are starting  BACnet-Tools MODE
