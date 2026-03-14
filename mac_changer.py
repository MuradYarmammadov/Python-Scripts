import subprocess
import argparse
import re
import os
import time

print("Initializing MAC Address Changer...")
time.sleep(1)


print(r"""
  __  __               _____ _                                 
 |  \/  |             / ____| |                                
 | \  / | __ _  ___  | |    | |__   __ _ _ __   __ _  ___ _ __ 
 | |\/| |/ _` |/ __| | |    | '_ \ / _` | '_ \ / _` |/ _ \ '__|
 | |  | | (_| | (__  | |____| | | | (_| | | | | (_| |  __/ |   
 |_|  |_|\__,_|\___|  \_____|_| |_|\__,_|_| |_|\__, |\___|_|   
                                                __/ |          
                                               |___/           by Murad Yarmammadov
""")
time.sleep(1.5)

def check_privs():
    if os.getuid() != 0:
        print("Error: You need root privileges to change a MAC address.")
        print("Please run the script again using 'sudo'.")
        exit(1)

def get_inputs():
    parser = argparse.ArgumentParser(description="A simple Python MAC changer.")

    parser.add_argument("-i","--interface", dest="interface", help="Interface to change its MAC address")
    parser.add_argument("-m","--mac_address", dest="mac_address", help="New MAC address to use")

    return parser.parse_args()


def control_inputs(interface,mac_address):
    if not interface:
        interface = input("Please enter the interface: ")
    if not mac_address:
        mac_address = input("Please enter the new MAC address: ")
    return interface,mac_address

def mac_changer(interface,mac_address):
    print(f"Changing MAC address for {interface} to {mac_address}...")
    try:
        subprocess.call(['ifconfig',interface,'down'])
        subprocess.call(['ifconfig',interface,'hw', 'ether',mac_address])
        subprocess.call(['ifconfig',interface,'up'])

    except subprocess.CalledProcessError:
        print(f"Error: Failed to change MAC address. Check if interface '{interface}' is correct.")
        exit(1)

def check_mac(interface):
    try:
        ifconfig = subprocess.check_output(['ifconfig',interface])
        ifconfig_str = ifconfig.decode()
        new_mac = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w",ifconfig_str)

        if new_mac:
            return new_mac.group(0)
        else:
            print("Mac Address Not Found")
            return False

    except subprocess.CalledProcessError:
        print(f"Error: Could not read interface '{interface}'. Are you sure it exists?")
        return False

check_privs()

user_inputs = get_inputs()
interface,mac_address = control_inputs(user_inputs.interface,user_inputs.mac_address)
mac_changer(interface,mac_address)

final_mac = check_mac(interface)
if final_mac == mac_address:
    print(f"MAC address for {interface} successfully changed to {final_mac}")
else:
    print("Error: MAC Address Not Changed")

