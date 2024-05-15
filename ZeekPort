#!/usr/bin/env python3

def add_zeekport_to_config(filename, zeekport):
    try:
        # Read the existing content of the file
        with open(filename, "r") as f:
            lines = f.readlines()

        # Check if the line already exists
        for line in lines:
            if line.strip() == f"Zeekport = {zeekport}":
                print(f"Line 'Zeekport = {zeekport}' already exists in {filename}.")
                return

        # Append the new line to the end of the file
        lines.append(f"Zeekport = {zeekport}\n")

        # Write the updated content back to the file
        with open(filename, "w") as f:
            f.writelines(lines)

        print(f"Added 'Zeekport = {zeekport}' to {filename}.")

    except FileNotFoundError:
        print(f"File {filename} not found. Make sure the file exists and the paths are set correctly.")

if __name__ == "__main__":
    zeekport_value = 8000
    zeekctl_config_file = "/opt/zeek/etc/zeekctl.cfg"
    add_zeekport_to_config(zeekctl_config_file, zeekport_value)
