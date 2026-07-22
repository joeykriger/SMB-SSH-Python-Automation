import subprocess
import getpass

def check_smb_access(ip, share, user, password):
    print(f"testing access to \\\\{ip}\\{share}...")

    # Use subprocess to call the native smbclient tool
    cmd = ['smbclient', f'//{ip}/{share}', '-U', f'{user}%{password}', '-c', 'ls']

    result = subprocess.run(cmd, capture_output = True, text = True)

    if result.returncode == 0:
        print("\nSUCCESS: SMB share is accessible. Contents:")
        print(result.stdout)
    else:
        print("\nFAILURE: Access Denied or Share Unavailable.")
        print(result.stderr)

if __name__ == "__main__":
    # For true automation, declare the actual username for win_user and actual password for win_pass
    win_user = input("Enter Windows Username (e.g., localadmin): ")
    win_pass = getpass.getpass("Enter Windows Password: ")
    check_smb_access("192.168.10.20", "WinShare", win_user, win_pass)