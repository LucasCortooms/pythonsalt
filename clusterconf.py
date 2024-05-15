#!/usr/bin/env python3
import subprocess

def get_network_interfaces():
    try:
        # Use the 'ip' command to detect network interfaces
        output = subprocess.check_output(["ip", "link", "show"], stderr=subprocess.DEVNULL)
        interfaces = [line.split(":")[1].strip() for line in output.decode("utf-8").splitlines() if ":" in line]
        return interfaces
    except subprocess.CalledProcessError:
        print("Cannot detect network interfaces.")
        return []

def has_ip_address(interface):
    try:
        # Use the 'ip' command to get the IP address of the interface
        output = subprocess.check_output(["ip", "addr", "show", interface], stderr=subprocess.DEVNULL)
        return "inet " in output.decode("utf-8")
    except subprocess.CalledProcessError:
        return False

def update_node_cfg():
    worker_sections = []
    interfaces = get_network_interfaces()
    for i, interface in enumerate(interfaces, start=1):
        if has_ip_address(interface):
            section = f"""
[worker-{i}]
type=worker
host=localhost
interface={interface}
"""
            worker_sections.append(section)

    config = f"""
[manager]
type=manager
host=localhost

[proxy-1]
type=proxy
host=localhost

{''.join(worker_sections)}
"""

    # Write the configuration to node.cfg
    try:
        with open("/opt/zeek/etc/node.cfg", "w") as cfg_file:
            cfg_file.write(config)
        print("Configuration updated in node.cfg.")
    except FileNotFoundError:
        print("Cannot find node.cfg. Make sure the file exists and the paths are set correctly.")

if __name__ == "__main__":
    update_node_cfg()
