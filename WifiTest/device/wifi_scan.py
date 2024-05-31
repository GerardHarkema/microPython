import network
from   binascii import hexlify
        # enable station interface and connect to WiFi access point
def _macAddrFromBSSID(bssid) :
    return hexlify(bssid, ':').decode().upper()

def _signalStrengthFromRSSI(rssi) :
    return 'Weak' if rssi < -70 else \
           'Fair' if rssi < -60 else \
           'Good' if rssi < -50 else \
           'Excellent'

# ------------------------------------------------------------------------------------

def _nameFromAuthCode(authCode) :
    if authCode == 0 :
        return 'OPEN'
    elif authCode == 1 :
        return 'WEP'
    elif authCode == 2 :
        return 'WPA-PSK'
    elif authCode == 3 :
        return 'WPA2-PSK'
    elif authCode == 4 :
        return 'WPA/WPA2-PSK'
    elif authCode == 5 :
        return 'WPA2 ENTERPRISE'
    elif authCode == 6 :
        return 'WPA3 PSK'
    elif authCode == 7 :
        return 'WPA2/WPA3 PSK'
    return 'UNKNOWN'

# ------------------------------------------------------------------------------------


nic = network.WLAN(network.STA_IF)
nic.active(True)
scan = nic.scan()
#for ssid in scan: print(str(ssid[0],'utf-8'))
i = 0
for x in scan :
    print(x)
    ssid     = x[0].decode('UTF-8')
    macaddr  = _macAddrFromBSSID(x[1])
    chan     = x[2]
    rssi     = x[3]
    signal   = _signalStrengthFromRSSI(rssi)
    authName = _nameFromAuthCode(x[4])
    hidden   = x[5]
    i += 1
    print('\n%02d> MAC address (BSSID) : %s' % (i, macaddr))
    if not hidden :
        print('    SSID                : %s' % ssid)
    else :
        print('    SSID (is hidden)    :')
    print('    Channel             : %s' % chan)
    print('    RSSI (signal)       : %s dBm (%s)' % (rssi, signal))
    print('    Authentication type : %s' % authName)

