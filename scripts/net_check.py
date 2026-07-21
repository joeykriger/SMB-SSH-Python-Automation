import subprocess
import socket
import datetime

#Target Configuration
WIN_IP = "192.168.10.20"
PORTS = {"SSH": 22, "SMB": 445}

def log_result(message):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("network_audit.log", "a") as log_file:
        log_file.write(f"[{timestamp}] {message}\n")
    print(message)

def test_ping(ip):
    response = subprocess.run(['ping', '-c', '1', '-W', '1', ip],
    stdout = subprocess.DEVNULL)
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