import pyboard
import os
from binascii import hexlify
import ast

class pyboard_tools:
    def __init__(self, com_port):
        self.pyb = pyboard.Pyboard(com_port, 115200)
        self.ST_MODE_FILE = 32768
        self.ST_MODE_DIR = 16384
        self.pyb.enter_raw_repl()
    # ------------------------------------------------------------------------------------

    def download_files_from_device(self, device_dir, local_dir):

        ret = self.pyb.fs_listdir(device_dir)

        for dir_result in ret:
            file = getattr(dir_result, 'name', None)
            st_mode = getattr(dir_result, 'st_mode', None)
            if st_mode == self.ST_MODE_FILE:
                device_file = device_dir + "/" + file
                text = "Download: " + device_file
                print(text)
                local_file = local_dir + "/" + file
                text = "      To: " + local_file
                print(text)
                self.pyb.fs_get(device_file, local_file)
            elif st_mode == self.ST_MODE_DIR:
                dir = file
                new_device_dir = device_dir + "/" +  dir
                new_local_dir = local_dir + "/" + dir
                if not os.path.isdir(new_local_dir):
                    text = "Creating local directory: " + new_local_dir
                    print(text)
                    os.mkdir(new_local_dir)
                self.download_files_from_device(new_device_dir, new_local_dir)
            else:
                print("Invalid file mode")
        print("Ready downloading!")
    # ------------------------------------------------------------------------------------

    def upload_files_to_device(self, local_dir, device_dir):
        dir_result = os.fsencode(local_dir)

        for file in os.listdir(local_dir):
            f = os.path.join(local_dir, file)
            # checking if it is a file
            if os.path.isfile(f):
                local_file = local_dir + "/" + file
                text = "Upload: " + local_file
                print(text)
                device_file = device_dir + "/" + file
                text = "    To: " + device_file
                print(text)
                self.pyb.fs_put(local_file, device_file)
            if os.path.isdir(f):
                dir = file
                new_local_dir = local_dir + "/" + dir
                new_device_dir = device_dir + "/" +  dir
                if not self.pyb.fs_exists(new_device_dir):
                    text = "Creating device directory: " + new_device_dir
                    print(text)
                    self.pyb.fs_mkdir(new_device_dir)
                self.upload_files_to_device(new_local_dir, new_device_dir)
        print("Ready uploading!")
    # ------------------------------------------------------------------------------------

    def clean_device(self, device_dir):
        ret = self.pyb.fs_listdir(device_dir)

        for dir_result in ret:
            file = getattr(dir_result, 'name', None)
            st_mode = getattr(dir_result, 'st_mode', None)
            if st_mode == self.ST_MODE_FILE:
                device_file = device_dir + "/" + file
                text = "Removing: " + device_file
                print(text)
                self.pyb.fs_rm(device_file)
            elif st_mode == self.ST_MODE_DIR:
                dir = file
                new_device_dir = device_dir + "/" +  dir
                self.clean_device(new_device_dir)
                text = "Removing device directory: " + new_device_dir
                print(text)
                self.pyb.fs_rmdir(new_device_dir)
            else:
                print("Invalid file mode")
        print("Restoring boot.py")
        self.pyb.fs_put("./boot.py", "./boot.py")
        print("Ready cleaning!")
    # ------------------------------------------------------------------------------------

    def connect_to_wifi(self, ssid, password):
        self.pyb.exec("import network")
        # enable station interface and connect to WiFi access point
        self.pyb.exec("nic = network.WLAN(network.STA_IF)")
        self.pyb.exec("nic.active(True)")
        wifi_connect = 'result = nic.connect("' + ssid + '", "' + password + '")'
        #print(wifi_connect)
        self.pyb.exec(wifi_connect)
        print("Connected to Wifi")
    # ------------------------------------------------------------------------------------

    def create_wifi_acces_point(self, ssid, password):
        self.pyb.exec("import network")
        # enable station interface and connect to WiFi access point
        self.pyb.exec("nic = network.WLAN(network.AP_IF)")
        self.pyb.exec("nic.active(True)")
        wifi_connect = 'result = nic.config(essid="' + ssid + '", password="' + password + '")'
        #print(wifi_connect)
        self.pyb.exec(wifi_connect)
        print("Wifi access point created")
    # ------------------------------------------------------------------------------------

    def scan_wifi(self):
        print( "Scanning wifi networks")
        self.pyb.exec("import network")
        # enable station interface and connect to WiFi access point
        self.pyb.exec("nic = network.WLAN(network.STA_IF)")
        self.pyb.exec("result = nic.active(True)")
        self.pyb.exec("print(result)")
        scan = self.pyb.exec("result = print(nic.scan())")
        scan_tuple = ast.literal_eval(scan.decode('utf-8'))

        i = 0
        for wifi_data in scan_tuple:
            ssid = wifi_data[0].decode('UTF-8', errors='ignore')
            mac = wifi_data[1]
            chan = int(wifi_data[2])
            rssi = int(wifi_data[3])
            auth = wifi_data[4]
            hidden = wifi_data[5]
            i += 1
            macaddr = self._macAddrFromBSSID(mac)
            print('%02d> MAC address (BSSID) : %s' % (i, macaddr))
            print('    Channel             : %s' % chan)
            if not hidden:
                print('    SSID                : %s' % ssid)
            else:
                print('    SSID                : (is hidden)')
            signal = self._signalStrengthFromRSSI(rssi)
            print('    RSSI (signal)       : %s dBm (%s)' % (rssi, signal))
            authName = self._nameFromAuthCode(auth)
            print('    Authentication type : %s\n' % authName)
        print("Done scanning  networks")
    # ------------------------------------------------------------------------------------

    def _signalStrengthFromRSSI(self, rssi):
        return 'Weak' if rssi < -70 else \
            'Fair' if rssi < -60 else \
                'Good' if rssi < -50 else \
                    'Excellent'
    # ------------------------------------------------------------------------------------
    def _nameFromAuthCode(self, authCode):
        if authCode == 0:
            return 'OPEN'
        elif authCode == 1:
            return 'WEP'
        elif authCode == 2:
            return 'WPA-PSK'
        elif authCode == 3:
            return 'WPA2-PSK'
        elif authCode == 4:
            return 'WPA/WPA2-PSK'
        elif authCode == 5:
            return 'WPA2 ENTERPRISE'
        elif authCode == 6:
            return 'WPA3 PSK'
        elif authCode == 7:
            return 'WPA2/WPA3 PSK'
        return 'UNKNOWN'
    # ------------------------------------------------------------------------------------
    def _macAddrFromBSSID(self, bssid):
        return hexlify(bssid, ':').decode().upper()
    # ------------------------------------------------------------------------------------

    def __del__(self):
        self.pyb.exit_raw_repl()

