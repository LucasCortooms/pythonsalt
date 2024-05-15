#!/usr/bin/env python3
import subprocess
import netifaces as ni

def clear_file(filename):
    # Clear the contents of the specified file
    with open(filename, "w") as f:
        f.truncate(0)

def get_network_info():
    try:
        # Get subnet information
        subnet_cmd = "ip -o -f inet addr show | awk '{print $4}'"
        subnets = subprocess.check_output(subnet_cmd, shell=True).decode().splitlines()

        # Create a dictionary to store subnet-interface mappings
        subnet_interface_map = {}

        # Get all available interface names
        interface_names = ni.interfaces()

        # Assign interfaces to subnets
        for subnet in subnets:
            # Remove the last octet (number) from the subnet
            subnet_without_last_octet = ".".join(subnet.split(".")[:-1])
            # Append ".0" to the modified subnet
            modified_subnet = subnet_without_last_octet + ".0"

            # Choose an interface (you can modify this part)
            interface_name = interface_names.pop(0) if interface_names else "default_interface"

            subnet_interface_map[modified_subnet] = interface_name

        # Clear the existing contents of networks.cfg
        clear_file("/opt/zeek/etc/networks.cfg")

        # Append the entries to networks.cfg
        with open("/opt/zeek/etc/networks.cfg", "a") as zeek_cfg:
            for subnet, interface in subnet_interface_map.items():
                zeek_cfg.write(f"{subnet}/24\t{interface}\n")  # Modify the CIDR notation as needed

        print("Modified subnets (ending with .0) with CIDR notation added to networks.cfg successfully!")

    except Exception as e:
        print(f"Error adding modified subnets to networks.cfg: {e}")

if __name__ == "__main__":
    get_network_info()
