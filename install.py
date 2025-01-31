import sys
import subprocess
import os
import json
from datetime import datetime
import requests
from urllib.parse import quote

def check_dependencies():
    print("Checking dependencies...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        return True
    except subprocess.CalledProcessError:
        print("ERROR: Failed to install dependencies.")
        return False
    except FileNotFoundError:
        print("ERROR: requirements.txt not found.")
        return False

def get_script_path():
    return os.path.abspath("monitor.py")

def search_servers(term):
    term_encoded = quote(term)
    url = f"https://www.speedtest.net/api/js/servers?engine=js&search={term_encoded}&limit=30"
    response = requests.get(url)
    if response.status_code == 200:
        try:
            return response.json()
        except requests.exceptions.JSONDecodeError:
            print("Error decoding server response")
            return None
    else:
        print("Error searching servers:", response.status_code)
        return None

def get_schedule_preferences():
    print("\nConfiguring speed test schedule")
    print("-----------------------------------------------------")
    
    schedule_types = {
        "1": ("MINUTE", "minutes"),
        "2": ("HOURLY", "hours"),
        "3": ("DAILY", "days")
    }
    
    while True:
        print("\nChoose execution frequency:")
        print("1. Every X minutes")
        print("2. Every X hours")
        print("3. Daily at specific time")
        
        choice = input("Choice (1-3): ").strip()
        
        if choice not in schedule_types:
            print("Invalid option. Please choose 1, 2 or 3.")
            continue
            
        schedule_type, unit = schedule_types[choice]
        
        if schedule_type in ("MINUTE", "HOURLY"):
            while True:
                if schedule_type == "MINUTE":
                    interval = input("Enter interval in minutes (1-1440) 1440 is 24 hours: ").strip()
                else:
                    interval = input("Enter interval in hours (1-24): ").strip()
                try:
                    interval = int(interval)
                    if (schedule_type == "MINUTE" and 1 <= interval <= 1440) or \
                       (schedule_type == "HOURLY" and 1 <= interval <= 24):
                        return schedule_type, interval
                    else:
                        print("Interval out of allowed range.")
                except ValueError:
                    print("Please enter a valid number.")
        else:  # DAILY
            while True:
                time = input("Enter execution time (HH:MM, example 14:30): ").strip()
                try:
                    datetime.strptime(time, "%H:%M")
                    return schedule_type, time
                except ValueError:
                    print("Invalid time format. Use HH:MM (example: 14:30)")

def get_server_preference():
    print("\nConfiguring speed test server")
    print("-----------------------------------------------------")
    
    while True:
        print("\nDo you want to:")
        print("1. Search for a specific server")
        print("2. Use automatic server selection")
        
        choice = input("Choice (1-2): ").strip()
        
        if choice == "1":
            while True:
                search_term = input("\nEnter server search term (city, provider, etc): ").strip()
                if not search_term:
                    print("Please enter a search term.")
                    continue
                
                print("Searching servers...")
                servers = search_servers(search_term)
                
                if not servers:
                    print("No servers found. Try another search term.")
                    continue
                
                print("\nFound servers:")
                for i, server in enumerate(servers, 1):
                    print(f"{i}. {server['sponsor']} - {server['name']} ({server['country']})")
                
                while True:
                    server_choice = input("\nChoose server number (or 0 to search again): ").strip()
                    try:
                        server_choice = int(server_choice)
                        if server_choice == 0:
                            break
                        if 1 <= server_choice <= len(servers):
                            chosen_server = servers[server_choice - 1]
                            return chosen_server
                        print("Invalid choice. Please choose a valid number.")
                    except ValueError:
                        print("Please enter a valid number.")
                
                if server_choice == 0:
                    continue
                break
        
        elif choice == "2":
            return None
        
        else:
            print("Invalid option. Please choose 1 or 2.")

def create_config_file(server_info):
    with open('config.json', 'w') as f:
        json.dump(server_info, f, indent=4)
    print("Configuration saved successfully!")

def create_task(schedule_type, interval):
    script_path = get_script_path()
    python_path = sys.executable
    task_name = "WanMonitor"
    
    # Build base command
    base_cmd = f'schtasks /Create /TN "{task_name}" /TR "{python_path} {script_path}" /F'
    
    if schedule_type == "MINUTE":
        schedule_cmd = f'{base_cmd} /SC MINUTE /MO {interval}'
    elif schedule_type == "HOURLY":
        schedule_cmd = f'{base_cmd} /SC HOURLY /MO {interval}'
    else:  # DAILY
        schedule_cmd = f'{base_cmd} /SC DAILY /ST {interval}'
    
    try:
        subprocess.run(schedule_cmd, check=True, shell=True)
        print("\nOK - Task scheduled successfully!")
        print(f"\nConfiguration details:")
        print(f"- Task name: {task_name}")
        print(f"- Script: {script_path}")
        if schedule_type == "MINUTE":
            print(f"- Execution: Every {interval} minutes")
        elif schedule_type == "HOURLY":
            print(f"- Execution: Every {interval} hours")
        else:
            print(f"- Execution: Daily at {interval}")
    except subprocess.CalledProcessError as e:
        print(f"\nERROR: Could not create scheduled task.")
        print("Make sure you are running the script as administrator.")
        print(f"Detailed error: {str(e)}")

def main():
    print("Speed Test Monitor Installation Assistant")
    print("======================================================")
    
    if not check_dependencies():
        return
    
    server_info = get_server_preference()
    config_path = create_config_file(server_info)
    
    schedule_type, interval = get_schedule_preferences()
    create_task(schedule_type, interval)
    
    print("\nInstallation completed!")
    if server_info:
        print(f"Selected server: {server_info['sponsor']} - {server_info['name']}")
    else:
        print("Using automatic server selection")
    print("To view results, check the 'results.html' file that will be created after first execution.")

if __name__ == "__main__":
    main()
