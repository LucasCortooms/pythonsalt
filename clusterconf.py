#!/usr/bin/env python3
import os
import subprocess

def get_network_interfaces():
    # Gebruik het 'ip' commando om de netwerkinterfaces te detecteren
    try:
        output = subprocess.check_output(["ip", "link", "show"], stderr=subprocess.DEVNULL)
        interfaces = [line.split(":")[1].strip() for line in output.decode("utf-8").splitlines() if ":" in line]
        return interfaces
    except subprocess.CalledProcessError:
        print("Kan netwerkinterfaces niet detecteren.")
        return []

def generate_worker_sections(interfaces):
    worker_sections = []
    for i, interface in enumerate(interfaces, start=1):
        section = f"""
[worker-{i}]
type=worker
host=localhost
interface={interface}
"""
        worker_sections.append(section)
    return "\n".join(worker_sections)

def update_node_cfg():
    config = f"""
[logger-1]
type=logger
host=localhost

[manager]
type=manager
host=localhost

[proxy-1]
type=proxy
host=localhost

{generate_worker_sections(get_network_interfaces())}
"""

    # Schrijf de configuratie naar node.cfg
    try:
        with open("/opt/zeek/etc/node.cfg", "w") as cfg_file:
            cfg_file.write(config)
        print("Configuratie is bijgewerkt in node.cfg.")
    except FileNotFoundError:
        print("Kan node.cfg niet vinden. Zorg ervoor dat het bestand bestaat en de juiste paden zijn ingesteld.")

if __name__ == "__main__":
    update_node_cfg()
