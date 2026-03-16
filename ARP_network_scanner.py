import time
import os
import scapy.all as scapy
import argparse
import ipaddress
import sys

print("Initializing ARP Network Scanner...")
time.sleep(1)

print(r"""
  ___  ____________   _   _      _                      _      _____                                 
 / _ \ | ___ \ ___ \ | \ | |    | |                    | |    /  ___|                                
/ /_\ \| |_/ / |_/ / |  \| | ___| |___      _____  _ __| | __ \ `--.  ___ __ _ _ __  _ __   ___ _ __ 
|  _  ||    /|  __/  | . ` |/ _ \ __\ \ /\ / / _ \| '__| |/ /  `--. \/ __/ _` | '_ \| '_ \ / _ \ '__|
| | | || |\ \| |     | |\  |  __/ |_ \ V  V / (_) | |  |   <  /\__/ / (_| (_| | | | | | | |  __/ |   
\_| |_/\_| \_\_|     \_| \_/\___|\__| \_/\_/ \___/|_|  |_|\_\ \____/ \___\__,_|_| |_|_| |_|\___|_|   
                                                                                                     
                                                                                                     by Murad Yarmammadov
""")
time.sleep(1.5)

def check_privs():
    if os.geteuid() != 0:
        print("Error: You need root privileges to run this script.")
        print("Please run the script again using 'sudo'.")
        sys.exit(1)

def ip_validation(ip_string):
    try:
        ipaddress.ip_network(ip_string, strict=False)
        return True
    except ValueError:
        return False

def get_input():
    parser = argparse.ArgumentParser(description="A simple ARP network scanner.")
    parser.add_argument("-i", "--ip", dest="ip_address", help="Target IP address or subnet (e.g., 192.168.1.0/24)")
    ip = parser.parse_args().ip_address

    if ip:
        if not ip_validation(ip):
            print(f"{ip} is not a valid IP address or subnet.")
            sys.exit(1)
    else:
        while True:
            ip = input("Enter an IP address or subnet: ")
            if ip_validation(ip):
                break
            else:
                print("Invalid format. Please try again (e.g., 10.0.0.1 or 192.168.1.0/24).")

    return ip

def network_scanner(ip_address):
    arp_request_packet = scapy.ARP(pdst=ip_address)
    broadcast_packet = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    full_packet = broadcast_packet/arp_request_packet

    (answered, unanswered)= scapy.srp(full_packet, timeout=1)
    print(answered.summary())

if __name__ == "__main__":
    check_privs()
    ip_address = get_input()
    network_scanner(ip_address)

