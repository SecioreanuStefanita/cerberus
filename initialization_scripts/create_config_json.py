import json
import shutil
import os

def get_user_input(prompt):
    return input(prompt)

def create_domain_config():
    # Collect user inputs for a single domain
    dns_name = get_user_input("Enter the DNS name (e.g., insomnia.local): ")
    target = get_user_input("Enter the target URL (e.g., http://localhost): ")
    ip = get_user_input("Enter the IP address (leave empty if none): ")
    port = int(get_user_input("Enter the port number (e.g., 1337): "))
    allowed_ips = get_user_input("Enter the allowed IPs (space-separated, leave empty if none): ").split()
    honeypot_path = get_user_input("Enter the honeypot path (e.g., /error/internal/errorCode=<errorCode>): ")
    honeypot_ips = get_user_input("Enter the honeypot IPs (space-separated, leave empty if none): ").split()
    honeypot_port = int(get_user_input("Enter the honeypot port number (e.g., 1338): "))

    # Create the dictionary structure for the domain
    domain_config = {
        dns_name: {
            "target": target,
            "ip": ip,
            "port": port,
            "allowed_ips": allowed_ips,
            "honeypot_path": honeypot_path,
            "honeypot_ips": honeypot_ips,
            "honeypot_port": honeypot_port
        }
    }

    return domain_config

def main():
    # Initialize an empty configuration dictionary
    config = {}
    
    # Collect configurations for multiple domains
    while True:
        domain_config = create_domain_config()
        config.update(domain_config)
        
        another = get_user_input("Do you want to add another domain? (yes/no): ").strip().lower()
        if another != 'yes':
            break

    # Write to routing_config.json
    config_path = "routing_config.json"
    with open(config_path, "w") as json_file:
        json.dump(config, json_file, indent=4)

    print("Configuration saved to routing_config.json")

    # Define target directories
    target_dirs = [
        "../request-checker-app",
        "../honeypot-app/config"
    ]

    # Copy the config file to the target directories
    for target_dir in target_dirs:
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        shutil.copy(config_path, os.path.join(target_dir, "routing_config.json"))
        print(f"Configuration copied to {target_dir}/routing_config.json")

if __name__ == "__main__":
    main()
