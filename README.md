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