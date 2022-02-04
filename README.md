# ASUTools
Это инструменты, которые созданы для использования в Linux системах без GUI, для инженеров АСУ ТП.
1. NET-SCANNER - сканирует локальные сети получает IP, MAC:, Vendor-Name. Все полученные данные выводятся в консоль и сохраняются в excel-file.
2. Modbus-Tester получает данные от устройств ModbusTCP. Все полученные данные выводятся в консоль и сохраняются в excel-file.
3. BACnet-Tools. 
    3.1 Сканирует сеть запросом Who-Is. Все полученные данные выводятся в консоль и сохраняются в excel-file.
    3.2 Получает object-list указанного device. Все полученные данные выводятся в консоль и сохраняются в excel-file.
    3.3 Запрашивает (present-value, status-flags, reliability) объектов( AI, AO, AV, BI, BO , BV, MSI, MSO,MSV). Все полученные данные выводятся в консоль и сохраняются в excel-file.

# Installations
cd /opt
git clone https://github.com/LutyiSan/ASUTool
cd /EASUTools
sudo sh install.sh
# Usage
cd /opt/EASUTools
python3 main.py -scan, so you are starting  NET-SCANNER MODE
python3 main.py -modbus, so you are starting  MODBUS-TESTER MODE
python3 main.py -bacnet, so you are starting  BACnet-Tools MODE
