import sys
import socket
import threading

# Global constant for filtering hexadecimal representations
HEX_FILTER = ''.join([(len(repr(chr(i))) == 3) and chr(i) or '.' for i in range(256)])

def hexdump(src, length=16, show=True):
    """Prints or returns a hexdump of the given data."""
    if isinstance(src, bytes):
        src = src.decode(errors="replace")
    results = []
    for i in range(0, len(src), length):
        segment = src[i:i+length]
        printable = segment.translate(HEX_FILTER)
        hexa = ' '.join(f'{ord(c):02X}' for c in segment)
        results.append(f'{i:04x}  {hexa:<{length*3}}  {printable}')
    if show:
        for line in results:
            print(line)
    else:
        return results

def receive_from(connection):
    """Receives data from a socket with a timeout."""
    buffer = b""
    connection.settimeout(5)
    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except Exception:
        pass
    return buffer

def request_handler(buffer):
    """Modify the request data (if needed)."""
    return buffer

def response_handler(buffer):
    """Modify the response data (if needed)."""
    return buffer

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    """Handles the proxy logic between local and remote connections."""
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

    remote_buffer = response_handler(remote_buffer)
    if len(remote_buffer):
        print("[<==] Sending %d bytes to localhost." % len(remote_buffer))
        client_socket.send(remote_buffer)

    while True:
        local_buffer = receive_from(client_socket)
        if len(local_buffer):
            print(f"[==>] Received {len(local_buffer)} bytes from localhost.")
            hexdump(local_buffer)
            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")

        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print(f"[<==] Received {len(remote_buffer)} bytes from remote.")
            hexdump(remote_buffer)
            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)
            print("[<==] Sent to localhost.")

        if not local_buffer and not remote_buffer:
            client_socket.close()
            remote_socket.close()
            print("[*] No more data. Closing connections.")
            break

def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    """Starts the server loop to accept client connections."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        server.bind((local_host, local_port))
        server.listen(5)
        print(f"[*] Listening on {local_host}:{local_port}")
    except Exception as e:
        print(f"[!!] Failed to bind to {local_host}:{local_port}. Error: {e}")
        sys.exit(0)

    while True:
        client_socket, addr = server.accept()
        print(f"[>] Received incoming connection from {addr[0]}:{addr[1]}")
        proxy_thread = threading.Thread(
            target=proxy_handler,
            args=(client_socket, remote_host, remote_port, receive_first)
        )
        proxy_thread.start()

def main():
    if len(sys.argv[1:]) != 5:
        print("Usage: ./proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]")
        sys.exit(0)

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])
    receive_first = sys.argv[5].lower() == "true"

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

if __name__ == '__main__':
    main()




'''
Let's break this down into simpler concepts and explanations to help you understand it more easily.

### **What is a TCP Proxy?**
A TCP (Transmission Control Protocol) proxy is like a "middleman" that relays data between two devices (such as a local machine and a remote server). This is helpful in different situations like monitoring traffic or altering the data being sent between them.

You might use a TCP proxy in these situations:
1. **Forwarding traffic**: Sending data from one device to another.
2. **Network assessments**: When you need to monitor or manipulate the data (e.g., penetration testing).

When testing networks in large companies, you may not always have the tools to directly inspect traffic, so a proxy helps by intercepting the data and letting you view or modify it.

### **Functions of the Proxy**
The proxy has several tasks that it performs:
1. **Hexdump**: Showing raw data in a human-readable way (both in hexadecimal and plain text).
2. **Receive Data**: Collecting data from either side (local or remote).
3. **Handle Traffic**: Passing data between the local machine and the remote server.
4. **Listening for Connections**: Setting up the proxy to listen for incoming connections.

### **Step-by-Step Breakdown**

1. **Imports and Hexdump Function:**

   The code starts by importing necessary modules (`sys`, `socket`, and `threading`), which are used for networking and threading tasks.

   - **Hexdump**: It prints the raw data in a readable format. For example, if the data is in a binary form, it translates it into both hexadecimal and ASCII characters, so it's easier to understand.

     Example:
     ```
     hexdump('python rocks\n and proxies roll\n')
     ```
     Would output something like this:
     ```
     0000  70 79 74 68 6F 6E 20 72 6F 63 6B 73 0A 20 61 6E   python rocks. an
     0010  64 20 70 72 6F 78 69 65 73 20 72 6F 6C 6C 0A      d proxies roll.
     ```
     This shows the byte values and their readable characters, making it easier to understand the data flowing through the proxy.

2. **Receiving Data (receive_from function):**

   This function handles receiving data from either the local machine or the remote machine.
   - It listens for incoming data and stores it in a `buffer` (like a container).
   - It sets a timeout (5 seconds by default) to avoid waiting forever.
   - The `buffer` is filled with data until there’s no more incoming data.

   The `recv(4096)` part reads up to 4096 bytes of data at a time.

3. **Handling Requests and Responses (request_handler and response_handler):**

   These functions are placeholders where you can modify the data before it gets sent.
   - **request_handler**: You can change the outgoing request before sending it to the remote server.
   - **response_handler**: You can change the incoming response before sending it back to the local machine.

   These functions are helpful if you want to test or manipulate the data (e.g., change user credentials or modify requests).

4. **Proxy Handler (proxy_handler function):**

   This function is the main "worker" of the proxy. It:
   - Connects to the remote server.
   - Receives data from the remote server (if needed).
   - Modifies the data using `response_handler` and sends it to the local client.
   - Continuously listens for data from both the local client and the remote server, forwarding data back and forth.

   This is the main function that performs the actual proxying between the two machines.

5. **Setting Up the Server (server_loop function):**

   - **server_loop**: This function listens for incoming connections on a local port and starts a new thread to handle each connection using the `proxy_handler` function.

   - **Socket Binding**: It binds the server to a local address (e.g., `127.0.0.1`) and listens for incoming connections on a specified port.
   - Each new incoming connection is handled by a new thread, allowing multiple connections to be processed simultaneously.

6. **Main Function (main):**

   - This is the entry point where you specify how to run the proxy by giving it arguments like:
     - `local_host`: Your local address (e.g., `127.0.0.1`).
     - `local_port`: The port your proxy will listen on (e.g., `9000`).
     - `remote_host`: The remote server address.
     - `remote_port`: The remote server’s port.
     - `receive_first`: Whether to receive data from the remote server before sending data from the client.

   - If the required arguments aren't provided, it shows how to use the script correctly.

---

### **Summary of the Key Components:**
- **Hexdump**: For printing data in readable format (hexadecimal and ASCII).
- **Receive Data**: Collects incoming data from the client or server.
- **Request and Response Handlers**: Modify the data before sending it.
- **Proxy Handler**: Handles the main logic of forwarding data between local and remote.
- **Server Loop**: Listens for incoming connections and starts a new thread for each connection.
- **Main Function**: Starts the proxy with the required parameters.

### **Why Use This Proxy?**
This proxy can be used for:
- Debugging unknown protocols.
- Modifying network traffic (e.g., changing requests or responses).
- Performing penetration tests to manipulate data sent over the network.

---

If you still have specific questions about any part of this or need further clarification, feel free to ask!
'''