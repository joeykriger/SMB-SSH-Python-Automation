
---

## CompTIA Troubleshooting 
*When you run your Python scripts, they will fail due to the sabotages you planted. Let's walk through the CompTIA 6-step methodology to fix them.*

---

### Ping Fails, SMB (445) is Closed *(Sabotage 1 & 2)*
* **Step 1: Identify the problem.** `net_check.py` reports Ping is unreachable, and ports 22 and 445 are closed. 
* **Step 2: Establish a theory.** (OSI Layer 3 and 7). Windows Firewall may be blocking ICMP and ports 22/445.
* **Step 3: Test the theory.** Run `ipconfig` on Windows - the IP address is `192.168.11.20`. Ubuntu is on `x.x.10.10` and Windows is on `x.x.11.20`. These are on different subnets. When Windows IP is corrected to `192.168.10.20`, ICMP and port 22 succeed. The theory shifts to Firewall to solve the port 445 failure. 
* **Step 4: Establish a plan.** There is an explicit Block rule for Port 445 in Windows Defender Firewall. Disable it to allow inbound port 445 traffic.
* **Step 5: Implement.** Open Defender, delete the Port 445 Block rule.
* **Step 6: Verify.** Run `net_check.py` again. Ping and Ports 22 and 445 now report SUCCESS.

---

### Windows SSH into Ubuntu Fails *(Sabotage 3)*
* **Step 1: Identify the problem.** From Windows, `ssh user@192.168.10.10` results in "Failed to connect".
* **Step 2: Establish a theory.** (OSI Layer 7 / Layer 4). The SSH service (daemon) is not inactive or disabled on Ubuntu.
* **Step 3: Test the theory.** On Ubuntu, run `systemctl status ssh`. The output shows "Inactive (dead)". Theory confirmed.
* **Step 4: Establish a plan.** Start and enable the SSH service.
* **Step 5: Implement.** Run `sudo systemctl start ssh` and `sudo systemctl enable ssh`.
* **Step 6: Verify.** Execute the SSH connection from Windows again. Success.

---

### Python SMB Script reports "Access Denied" *(Sabotage 4)*
* **Step 1: Identify the problem.** Running the script returns `Access Denied or Share Unavailable.` I expected the `SUCCESS` output to be displayed.
* **Step 2: Establish a theory.** The `WinShare` folder may have misconfigured permissions, or I forgot to share it on the Network Path.
* **Step 3: Test the theory.** Right-click the folder in Properties -> Sharing. The Sharing tab shows `WinShare` in on the Network Path. The Security tab shows the `Users` group has explicit `Deny` Read permission checked.
* **Step 4 & 5: Plan and Implement.** Uncheck the `Deny` permission, apply changes, and run the script again
* **Step 6: Verify.** Running the script again returns, `SUCCESS: SMB share is accessible.` The Ubuntu SMB client can now read files from the Windows SMB server.

---

## Key Takeaways
* *I designed an isolated virtual environment to test interoperability between Windows and Linux without jeopardizing a production network.*
* *Rather than just setting up file shares, I wrote Python scripts to act as a health-check monitor, simulating how a tech would verify service uptime at scale.*
* *I intentionally broke my own environment by messing with subnet masks, firewalls, and service states so I could practice structured troubleshooting using the CompTIA methodology.*
* *I prioritized using Python's standard library (`socket`, `subprocess`) to ensure my scripts could run anywhere without dependency management overhead.*

---
