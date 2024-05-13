#!/usr/bin/env python3
import subprocess
import netifaces as ni

def get_network_info():
    try:
        # Get subnet information
        subnet_cmd = "ip -o -f inet addr show | awk '{print $4}'"
        subnets = subprocess.check_output(subnet_cmd, shell=True).decode().splitlines()

        # Create a list of Zeek network entries
        zeek_networks = []
        for subnet in subnets:
            # Remove the last octet (number) from the subnet
            subnet_without_last_octet = ".".join(subnet.split(".")[:-1])
            # Append ".0" to the modified subnet
            modified_subnet = subnet_without_last_octet + ".0"

            # Get the corresponding interface name
            interface_names = ni.interfaces()
            interface_name = interface_names[0]  # Choose the first interface (you can modify this part)

            zeek_networks.append(f"{modified_subnet}\t{interface_name}")

        # Append the entries to networks.cfg
        with open("/opt/zeek/etc/networks.cfg", "a") as zeek_cfg:
            for entry in zeek_networks:
                zeek_cfg.write(entry + "\n")

        print("Modified subnets (ending with .0) added to networks.cfg successfully!")

    except Exception as e:
        print(f"Error adding modified subnets to networks.cfg: {e}")

if __name__ == "__main__":
    get_network_info()
