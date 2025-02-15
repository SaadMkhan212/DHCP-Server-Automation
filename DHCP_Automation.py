##################################
#Saad Khan
#Networking Automation Script with Python.
#The Script installs and configures the DHCP Server on Ubuntu/Debian Systems.
#It installs the dhcp server package and prompts the user to enter in the range, subnet, interface.
##################################
import os
import subprocess

def install_dhcp_server():
    print("Updating package list and installing ISC DHCP Server...")
    subprocess.run(["sudo", "apt", "update"], check=True)
    subprocess.run(["sudo", "apt", "install", "-y", "isc-dhcp-server"], check=True)
    
    subnet = input("Enter the subnet (e.g., 192.168.1.0): ")
    netmask = input("Enter the netmask (e.g., 255.255.255.0): ")
    range_start = input("Enter the DHCP range start (e.g., 192.168.1.100): ")
    range_end = input("Enter the DHCP range end (e.g., 192.168.1.200): ")
    interface = input("Enter the network interface (e.g., eth0): ")
    
    print("Configuring DHCP server...")
    dhcp_config = f"""default-lease-time 600;
max-lease-time 7200;
option subnet-mask {netmask};
option broadcast-address {subnet[:-1]}255;
option routers {subnet[:-1]}1;
option domain-name-servers 8.8.8.8, 8.8.4.4;
subnet {subnet} netmask {netmask} {{
  range {range_start} {range_end};
}} 
"""
    
    with open("/etc/dhcp/dhcpd.conf", "w") as f:
        f.write(dhcp_config)
    
    print("Setting up the DHCP server interface...")
    with open("/etc/default/isc-dhcp-server", "w") as f:
        f.write(f'INTERFACESv4="{interface}"\n')
    
    print("Restarting DHCP service...")
    subprocess.run(["sudo", "systemctl", "restart", "isc-dhcp-server"], check=True)
    subprocess.run(["sudo", "systemctl", "enable", "isc-dhcp-server"], check=True)
    
    print("DHCP server installation and configuration complete.")

if __name__ == "__main__":
    install_dhcp_server()