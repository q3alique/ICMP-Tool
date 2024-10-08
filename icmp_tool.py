import socket
import os
import struct
import sys
import time
import base64

# Constants for ICMP
ICMP_ECHO_REQUEST = 8

# ANSI color codes for terminal output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def checksum(source_string):
    """Calculate the checksum of the data."""
    count_to = (len(source_string) // 2) * 2
    sum = 0
    count = 0

    while count < count_to:
        this_val = source_string[count + 1] * 256 + source_string[count]
        sum = sum + this_val
        sum = sum & 0xffffffff
        count = count + 2

    if count_to < len(source_string):
        sum = sum + source_string[len(source_string) - 1]
        sum = sum & 0xffffffff

    sum = (sum >> 16) + (sum & 0xffff)
    sum = sum + (sum >> 16)
    answer = ~sum
    answer = answer & 0xffff
    answer = answer >> 8 | (answer << 8 & 0xff00)
    return answer

def create_icmp_packet(id, seq, data):
    """Create an ICMP packet."""
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, 0, id, seq)
    data = data.encode('utf-8')
    my_checksum = checksum(header + data)
    header = struct.pack('bbHHh', ICMP_ECHO_REQUEST, 0, socket.htons(my_checksum), id, seq)
    return header + data

def send_icmp_message(host, data, use_base64):
    """Send ICMP message."""
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    packet_id = os.getpid() & 0xFFFF
    
    if use_base64:
        # Base64 encode the message
        data = base64.b64encode(data.encode('utf-8')).decode('utf-8')
        print(f"{Colors.OKBLUE}Message encoded in Base64: {data}{Colors.ENDC}")

    packet = create_icmp_packet(packet_id, 1, data)
    sock.sendto(packet, (host, 1))
    print(f"{Colors.OKGREEN}ICMP packet sent to {host} with data: {data}{Colors.ENDC}")

def is_base64_encoded(data):
    """Check if a string is Base64 encoded."""
    try:
        if base64.b64encode(base64.b64decode(data)).decode('utf-8') == data:
            return True
        return False
    except Exception:
        return False

def receive_icmp_message(sock):
    """Receive ICMP message."""
    while True:
        packet, addr = sock.recvfrom(1024)
        ip_header = packet[:20]  # IP header is the first 20 bytes
        icmp_header = packet[20:28]  # ICMP header is the next 8 bytes
        
        icmp_type, code, checksum, packet_id, sequence = struct.unpack('bbHHh', icmp_header)
        
        print(f"{Colors.HEADER}Received packet from {addr[0]}{Colors.ENDC}")
        print(f"ICMP Type: {icmp_type}, Code: {code}, Checksum: {checksum}, ID: {packet_id}, Sequence: {sequence}")
        
        # Check if the packet is an ICMP echo request (Type 8)
        if icmp_type == ICMP_ECHO_REQUEST:
            payload = packet[28:].decode('utf-8')
            
            # Check if the payload is Base64 encoded
            if is_base64_encoded(payload):
                decoded_payload = base64.b64decode(payload).decode('utf-8')
                print(f"{Colors.OKBLUE}Received Base64 encoded payload: {payload}{Colors.ENDC}")
                print(f"{Colors.OKGREEN}Decoded Base64 message: {decoded_payload}{Colors.ENDC}")
            else:
                print(f"{Colors.OKGREEN}Received plain message: {payload}{Colors.ENDC}")
            
            break
        else:
            print(f"Received unexpected ICMP packet: Type {icmp_type}, Code {code}")

def client_mode(target_ip, message, use_base64):
    """Client mode to send data."""
    print(f"Sending data to {target_ip}: {message}")
    send_icmp_message(target_ip, message, use_base64)
    time.sleep(1)

def server_mode():
    """Server mode to receive data."""
    print("Listening for incoming ICMP packets...")
    sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    while True:
        receive_icmp_message(sock)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"{Colors.WARNING}Usage:{Colors.ENDC}")
        print("  --client <target_ip> <message> [--b64]  : Run as client to send ICMP messages (optionally Base64 encoded).")
        print("  --server                                : Run as server to listen for ICMP messages.")
        sys.exit(1)

    mode = sys.argv[1]

    if mode == "--client":
        if len(sys.argv) < 4:
            print(f"{Colors.FAIL}Usage for client mode: python3 script.py --client <target_ip> <message> [--b64]{Colors.ENDC}")
            sys.exit(1)
        
        target_ip = sys.argv[2]
        message = sys.argv[3]
        use_base64 = '--b64' in sys.argv
        client_mode(target_ip, message, use_base64)

    elif mode == "--server":
        server_mode()
    
    else:
        print(f"{Colors.FAIL}Invalid option. Use --client or --server.{Colors.ENDC}")
        sys.exit(1)
