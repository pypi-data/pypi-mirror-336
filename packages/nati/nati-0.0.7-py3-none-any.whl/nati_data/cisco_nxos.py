
from nati.ssh_connector import get_device_info
from nati.config import load_config
import re
import sqlite3
from nati_data.config_loader import load_project_config

def load_seed_devices(filename="seedfile.txt"):
    """Load devices from seed file."""
    with open(filename, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def get_interfaces(conn):
    """Get interface IP addresses."""
    output = conn.send_command("show ip interface brief")
    interfaces = []
    for line in output.splitlines():
        if re.search(r'\d+\.\d+\.\d+\.\d+', line):
            interfaces.append(line.strip())
    return interfaces

def discover_devices():
    # Load configuration
    config = load_config()
    username = config['nxos']['uid']
    password = config['nxos']['pwd']
    
    # Load devices from seed file
    devices = load_seed_devices()
    
    print("\nCisco NXOS Device Discovery")
    print("=" * 50)
    
    for device in devices:
        print(f"\nChecking device: {device}")
        try:
            from netmiko import ConnectHandler
            device_params = {
                "device_type": "cisco_nxos",
                "host": device,
                "username": username,
                "password": password,
            }
            
            with ConnectHandler(**device_params) as conn:
                hostname = conn.send_command("show hostname").strip()
                serial = conn.send_command("show inventory | include SN:").split("SN: ")[-1].strip()
                interfaces = get_interfaces(conn)
                
                print(f"Hostname: {hostname}")
                print(f"Serial Number: {serial}")
                print("Interfaces:")
                for interface in interfaces:
                    print(f"  {interface}")
                
                # Save to database
                db_config = load_project_config()
                db_path = db_config.get("filename")
                
                with sqlite3.connect(db_path) as db:
                    cursor = db.cursor()
                    cursor.execute("""
                        INSERT INTO devices (name, ip_address, serial_number)
                        VALUES (?, ?, ?)
                    """, (hostname, device, serial))
                    db.commit()
                print(f"[+] Device {hostname} saved to database")
                
        except Exception as e:
            print(f"Error connecting to {device}: {str(e)}")

if __name__ == "__main__":
    discover_devices()
