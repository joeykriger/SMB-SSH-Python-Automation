import subprocess

def check_smb_access(ip, share, user):
    print(f"testing access to \\\\{ip}\\{share}...")

    # Use subprocess to call the native smbclient tool
    cmd = ['smbclient', f'//{ip}/{share}', '-U', f'{user}', '-c', 'ls']

    result = subprocess.run(cmd, capture_output = True, text = True)

    if result.returncode == 0:
        print("\nSUCCESS: SMB share is accessible. Contents:")
        print(result.stdout)
    else:
        print("\nFAILURE: Access Denied or Share Unavailable.")
        print(result.stderr)

if __name__ == "__main__":
    win_user = input("Enter Windows Username (e.g., localadmin): ")
    check_smb_access("192.168.10.20", "WinShare", win_user)