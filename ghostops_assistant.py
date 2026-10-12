import subprocess
import sys
import time

def run_command(command):
    """Runs a shell command and returns its output."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error executing command '{command}': {e}", file=sys.stderr)
        return None

def check_service_status(service_name):
    """Checks the status of a given systemd service."""
    print(f"Checking status for service: {service_name}...")
    command = f"systemctl is-active {service_name}"
    status = run_command(command)
    if status == "active":
        print(f"'{service_name}' is running.")
        return True
    else:
        print(f"'{service_name}' is not running. Status: {status}")
        return False

def restart_service(service_name):
    """Restarts a given systemd service."""
    print(f"Attempting to restart service: {service_name}...")
    command = f"sudo systemctl restart {service_name}"
    output = run_command(command)
    if output is not None:
        print(f"Restart command executed for '{service_name}'.")
        # Give service a moment to restart
        time.sleep(5)
        # Verify restart
        if check_service_status(service_name):
            print(f"'{service_name}' successfully restarted.")
        else:
            print(f"Failed to confirm restart for '{service_name}'.")
    else:
        print(f"Failed to execute restart command for '{service_name}'.")

def main():
    """Main function to simulate autonomous SRE tasks."""
    print("--- GhostOps: Autonomous Linux Terminal SRE Assistant ---")

    # Example: Monitor and restart a critical service if it's down
    critical_service = "nginx" # Replace with a service name on your system

    if not check_service_status(critical_service):
        print(f"'{critical_service}' is down. Initiating autonomous recovery.")
        restart_service(critical_service)
    else:
        print(f"'{critical_service}' is healthy. No action needed.")

    # Example: Check disk space (simplified)
    print("\nChecking disk usage...")
    df_output = run_command("df -h /")
    if df_output:
        print(df_output)
        # In a real scenario, you'd parse this and trigger alerts if usage is high.

    print("\nGhostOps simulation complete.")

if __name__ == "__main__":
    main()
