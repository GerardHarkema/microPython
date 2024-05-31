import network
ssid = "myMicroPython"
password = ""
ap = network.WLAN(network.AP_IF)
ap.active(True)
ap.config(essid=ssid, password=password)