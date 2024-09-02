#Wlan-Scanner

import os
import re
import subprocess

def scan_wifi():
    #Run the iwlist command to scan for Wifi networks
    cmd = subprocess.Popen(['iwlist', 'wlan0', 'scan'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = cmd.communicate()

    if err:
        print('Error scanning for Wifi networks')
        return

    #Decode the output from bytes to string
    out = out.decode('utf-8')

    # Regular expressions to find the necessary fields
    ssid_regex = re.compile(r'ESSID:"([^"]+)"')
    signal_level_regex = re.compile(r'Signal level=(-?\d+) dBm')
    encryption_regex = re.compile(r'Encryption key:(on|off)')

    networks = []
    for ssid, signal, enc in zip(re.findall(ssid_regex, out), re.findall(signal_level_regex, out), re.findall(encryption_regex, out)):
        networks.append({'SSID': ssid, 'Signal': signal, 'Encryption': enc == 'on'})

    return networks

if __name__ == '__main__':
    networks = scan_wifi()

    if networks:
        print('Avialable WiFI networks: ')
        print('SSID'.ljust(30) + 'Signal'.ljust(15) + 'Encryption')
        for network in networks:
            print(f"{network['SSID'].ljust(30)} {network['Signal'].ljust(15)} {'Yes' if network['Encryption'] else 'No'}")

    else:
        print('No networks found')        