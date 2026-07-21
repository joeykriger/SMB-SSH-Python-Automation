# Portfolio Project: Cross-Platform SMB & SSH Automation with Python

## 1. Scenario Overview
In this lab, we build a completely isolated, two-node virtual network to simulate a heterogeneous enterprise environment. The scenario bridges a Windows 11 Home machine with an Ubuntu Linux Desktop machine to facilitate bi-directional file sharing (SMB) and remote administration (SSH). 

As an IT Support Technician, manual administration doesn't scale. To demonstrate automation capabilities, this lab focuses on building Python scripts using only the standard library to verify network health, audit SMB/SSH configurations, and securely copy files. Intentional sabotages are introduced to simulate a broken environment, allowing us to utilize the CompTIA troubleshooting methodology and OSI model to restore full functionality.

## 2. Skills Demonstrated
* **Networking & Infrastructure:** Static IPv4 configuration, VirtualBox Internal Networking, ICMP/TCP port testing.
* **Systems Administration:** Bi-directional OpenSSH configuration, SMB/Samba file sharing across OS boundaries, Windows and Linux (UFW) firewall configuration, NTFS and Linux file permissions.
* **Automation (Python):** Native network socket testing, `subprocess` remote command execution, file manipulation, SHA-256 hashing, and automated logging.
* **Troubleshooting:** CompTIA 6-step methodology, OSI layer isolation.

## 3. Technologies Used
* **Hypervisor:** Oracle VirtualBox
* **Operating Systems:** Windows 11 Home, Ubuntu Desktop 22.04/24.04 LTS
* **Protocols:** IPv4, ICMP, TCP, SSH (Port 22), SMB (Port 445)
* **Languages & Tools:** Python 3 (Standard Library), OpenSSH, Samba, PowerShell, Bash

## 4. Learning Objectives
1. Configure an isolated host-only network between Windows and Linux.
2. Establish secure, bi-directional remote command execution and file sharing.
3. Write beginner-friendly Python scripts to automate daily help desk monitoring tasks.
4. Methodically troubleshoot network and service misconfigurations using industry standards.

---

## 5. Pre-Lab: VirtualBox & Network Setup
*Note: Your physical host machine must remain completely isolated from this environment.*

### Step 5.1: VirtualBox "LabNet" Configuration
1. Open VirtualBox Manager.
2. Go to **Settings** for *both* VMs -> **Network**.
3. Change **Attached to:** to **Internal Network**.
4. Set the **Name:** to `LabNet`.
5. Ensure Promiscuous Mode is set to **Deny** and Cable Connected is **Checked**.

### Step 5.2: Static IP Configuration
**Windows 11 Home VM:**
1. Open **Network Connections** (`ncpa.cpl`).
2. Right-click your adapter -> **Properties** -> **IPv4**.
3. Set IP address: `192.168.10.20`
4. Set Subnet mask: `255.255.255.0`
5. Leave Gateway/DNS blank (isolated network).

**Ubuntu Desktop VM:**
1. Navigate to the **Netplan YAML** for the **internal network** adapter.
2. Set the static address: `192.168.10.10/24`.
3. Use **#** to comment out the **dhcp4** configuration section.
4. **Save** and **Exit** the YAML file.

---

## 6. The Intentional Sabotages (Setup Phase)
To practice troubleshooting later, intentionally misconfigure the following items during your setup:
1. **The Subnet Sabotage:** On the Windows VM, change the Subnet mask to `255.255.255.128` (instead of 255.255.255.0). 
2. **The Firewall Sabotage:** On Windows, create a Windows Defender Firewall rule explicitly **Blocking** inbound traffic on TCP Port 445.
3. **The Service Sabotage:** On Ubuntu, stop and disable the SSH service: `sudo systemctl stop ssh` and `sudo systemctl disable ssh`.
4. **The Permission Sabotage:** On Windows, remove "Read" permissions for the shared SMB folder under the NTFS Security tab (leave Share permissions intact).

---

## 7. Step-by-Step Instructions: Services

### 7.1: Bi-Directional SSH Configuration
**On Windows 11 Home:**
1. Open **Settings** -> **Apps** -> **Optional Features**.
2. Click **View features**, search for **OpenSSH Server**, and install it.
3. Open an Administrator PowerShell prompt:
   * `Start-Service sshd`
   * `Set-Service -Name sshd -StartupType 'Automatic'`
   
**On Ubuntu Desktop:**
1. Open terminal: `sudo apt update && sudo apt install openssh-server -y`
2. *(Normally we would start it here, but remember Sabotage #3!)*

### 7.2: Bi-Directional SMB Configuration
**On Windows 11 Home:**
1. Create a folder `C:\WinShare`.
2. Right-click -> **Properties** -> **Sharing** -> **Advanced Sharing**.
3. Check **Share this folder**. Click **Permissions**, grant **Everyone -> Full Control**.
4. *(Remember Sabotage #4: The Security tab permissions are deliberately broken).*

**On Ubuntu Desktop:**
1. Install Samba: `sudo apt install samba -y`
2. Create a folder: `mkdir ~/UbuntuShare`
3. Edit the config: `sudo nano /etc/samba/smb.conf` and append:
   ```ini
   [UbuntuShare]
   path = /home/username/UbuntuShare
   read only = no
   guest ok = yes
   ```
4. Restart Samba: `sudo systemctl restart smbd`

---

## 8. Python Automation Tasks
As an IT tech, you need tools to verify environment health. Since you have minimal Python experience, these scripts are built to be beginner-friendly, heavily commented, and use **only the Python standard library**. 

Create these files on your Ubuntu VM. 

### Script 1: Network Health Checker (`net_check.py`)
This script automates Layer 3 (Ping) and Layer 4 (Port socket) checks to verify baseline connectivity.

```python
import subprocess
import socket
import datetime

# Target Configuration
WIN_IP = "192.168.10.20"
PORTS = {"SSH": 22, "SMB": 445}

def log_result(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("network_audit.log", "a") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")
    print(message)

def test_ping(ip):
    # -c 1 means send 1 packet. (On windows, this would be -n 1)
    response = subprocess.run(['ping', '-c', '1', '-W', '1', ip], stdout=subprocess.DEVNULL)
    if response.returncode == 0:
        log_result(f"SUCCESS: {ip} is reachable via ICMP (Ping).")
    else:
        log_result(f"FAILURE: {ip} is UNREACHABLE via ICMP (Ping).")

def test_port(ip, port, service_name):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(2)
    try:
        s.connect((ip, port))
        log_result(f"SUCCESS: {service_name} (Port {port}) is OPEN on {ip}.")
    except Exception as e:
        log_result(f"FAILURE: {service_name} (Port {port}) is CLOSED/FILTERED on {ip}.")
    finally:
        s.close()

if __name__ == "__main__":
    log_result("--- STARTING NETWORK HEALTH CHECK ---")
    test_ping(WIN_IP)
    for service, port in PORTS.items():
        test_port(WIN_IP, port, service)
```

### Script 2: SSH Automation Script (`ssh_deploy.py`)
This script uses the native OS SSH client to execute a remote command (e.g., check disk space) without requiring third-party libraries like Paramiko.

```python
import subprocess

def run_remote_command(ip, user, command):
    print(f"Connecting to {user}@{ip} to run: '{command}'...")
    
    # We use subprocess to call the system's native SSH client
    ssh_cmd = ['ssh', '-o', 'StrictHostKeyChecking=no', f'{user}@{ip}', command]
    
    try:
        result = subprocess.run(ssh_cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("\n--- COMMAND OUTPUT ---")
            print(result.stdout)
        else:
            print("\n--- ERROR ---")
            print(result.stderr)
    except subprocess.TimeoutExpired:
        print("Error: SSH connection timed out.")

if __name__ == "__main__":
    # Note: Ensure you have set up SSH keys for true automation, 
    # otherwise it will prompt for a password in the terminal!
    win_user = input("Enter Windows Username: ")
    run_remote_command("192.168.10.20", win_user, "ipconfig")
```

---

## 9. CompTIA Troubleshooting Walkthrough
*When you run your Python scripts, they will fail due to the sabotages you planted. Let's walk through the CompTIA 6-step methodology to fix them.*

### Sabotage 1 & 2: Ping Fails, SMB (445) is Closed
* **Step 1: Identify the problem.** `net_check.py` reports Ping is unreachable and Port 445 is closed. 
* **Step 2: Establish a theory.** (OSI Layer 3). Ping relies on correct IP addressing and subnet masks. Alternatively, Windows Firewall is blocking it.
* **Step 3: Test the theory.** Run `ipconfig` on Windows. Wait, the subnet mask is `255.255.255.128`. Ubuntu is on `.10` and Windows is on `.20`. Under `/25`, these are in the same subnet. Ping should work. The theory shifts to Firewall. 
* **Step 4: Establish a plan.** Disable the explicit Block rule for Port 445 in Windows Defender Firewall and allow ICMP Echo Requests.
* **Step 5: Implement.** Open `wf.msc`, delete the Port 445 Block rule, and enable "File and Printer Sharing (Echo Request - ICMPv4-In)".
* **Step 6: Verify.** Run `net_check.py` again. Ping and Port 445 now report SUCCESS.

### Sabotage 3: Windows SSH into Ubuntu Fails
* **Step 1: Identify the problem.** From Windows, `ssh user@192.168.10.10` results in "Connection refused".
* **Step 2: Establish a theory.** (OSI Layer 7 / Layer 4). The SSH service (daemon) is not running on Ubuntu.
* **Step 3: Test the theory.** On Ubuntu, run `systemctl status ssh`. The output shows "Inactive (dead)". Theory confirmed.
* **Step 4: Establish a plan.** Start and enable the SSH service.
* **Step 5: Implement.** Run `sudo systemctl start ssh` and `sudo systemctl enable ssh`.
* **Step 6: Verify.** Execute the SSH connection from Windows again. Success.

### Sabotage 4: Python SMB Script reports "Access Denied"
* **Step 1: Identify the problem.** You can see the `\WinShare` folder, but cannot read files inside it. 
* **Step 2: Establish a theory.** Share permissions allow everyone, but NTFS (Security) permissions are restrictive. 
* **Step 3: Test the theory.** Right-click the folder in Windows -> Security. Notice "Read" is missing for the user attempting to access it.
* **Step 4 & 5: Plan and Implement.** Edit the NTFS permissions to allow Read/Write for the required user.
* **Step 6: Verify.** File transfers now complete successfully.

---

## 10. OSI Layer Analysis
This lab directly exercises multiple layers of the OSI model:
* **Layer 1 (Physical):** Simulated via VirtualBox's virtual network adapter and "Cable Connected" status. 
* **Layer 2 (Data Link):** MAC address resolution (ARP) occurs on the `LabNet` virtual switch.
* **Layer 3 (Network):** Static IPv4 assignment (`192.168.10.10` and `.20`) and ICMP (Ping) diagnostics.
* **Layer 4 (Transport):** Utilizing TCP Port 22 (SSH) and TCP Port 445 (SMB) for communication.
* **Layer 7 (Application):** OpenSSH daemon, Samba daemon, and Python scripts interacting with network sockets.

---

## 11. Common Mistakes
* **Assuming Ping = Open Service:** A machine might reply to a ping (Layer 3), but the SSH or SMB port might be closed (Layer 4/7). 
* **Share vs. NTFS Permissions:** In Windows, the *most restrictive* permission between the "Sharing" tab and the "Security" (NTFS) tab wins. 
* **Subprocess execution stalling:** When using `subprocess` in Python to automate SSH, if host-key checking isn't disabled (`-o StrictHostKeyChecking=no`), the script will hang indefinitely waiting for a hidden `Y/N` terminal prompt.

---

## 12. Key Takeaways
* *I designed an isolated virtual environment to test interoperability between Windows and Linux without jeopardizing a production network.*
* *Rather than just setting up file shares, I wrote Python scripts to act as a health-check monitor, simulating how a tech would verify service uptime at scale.*
* *I intentionally broke my own environment—messing with subnet masks, firewalls, and service states—so I could practice structured troubleshooting using the CompTIA methodology.*
* *I prioritized using Python's standard library (`socket`, `subprocess`) to ensure my scripts could run anywhere without dependency management overhead.*

---