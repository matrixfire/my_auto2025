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
        if remote_buffer:
            hexdump(remote_buffer)
            remote_buffer = response_handler(remote_buffer)
            client_socket.send(remote_buffer)

    while True:
        local_buffer = receive_from(client_socket)
        if local_buffer:
            print(f"[==>] Received {len(local_buffer)} bytes from localhost.")
            hexdump(local_buffer)
            local_buffer = request_handler(local_buffer)
            remote_socket.send(local_buffer)
            print("[==>] Sent to remote.")

        remote_buffer = receive_from(remote_socket)
        if remote_buffer:
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
