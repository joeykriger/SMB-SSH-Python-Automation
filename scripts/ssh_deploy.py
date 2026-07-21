import subprocess

def run_remote_command(ip, user, command):
    print(f"Connecting to {user}@{ip} to run: '{command}'...")

    # Use subprocess to call the system's native SSH client
    ssh_cmd = ['ssh', '-o', 'StrictHostKeyChecking=no', f'{user}@{ip}', command]

    try:
        result = subprocess.run(ssh_cmd, capture_output = True, text = True, timeout = 10)
        if result.returncode == 0:
            print("\n--- COMMAND OUTPUT ---")
            print(result.stdout)
        else:
            print("--- ERROR ---")
            print(result.stderr)
    except subprocess.TimeoutExpired:
        print("Error: SSH connection timed out.")

if __name__ == "__main__":
    # Ensure SSH keys are set up for true automation, otherwise it will prompt for a password in the terminal.
    win_user = input("Enter Windows Username: ")
    run_remote_command("192.168.10.20", win_user, "ipconfig")