'''
Your code is an implementation of a NetCat-like tool, which is used for networking tasks like 1)sending and receiving data, 2)file transfer, 3)executing commands remotely, and 3)opening a remote command shell. 
It combines socket programming with functionality for both server (listen) and client (send) roles.


Modes of Operation:
    listen mode (-l): Allows it to accept incoming connections and act as a server.
    send mode (default): Sends data to a remote server.

Additional Functionalities:
    Execute a command remotely (-e flag).
    Upload a file to the server (-u flag).
    Open a command shell (-c flag).

    

https://chatgpt.com/c/67467509-8300-8007-9e68-71fb4e9e6d61

LEARN:
The recv call is blocking, meaning it will wait for data if none is immediately available.
If data is received, it is appended to the file_buffer using file_buffer += data.
If data is empty (indicating the client has finished sending), the loop terminates.


.encode() converts the string into bytes, as sockets only transmit byte data.



The choice of 4096 bytes as a chunk size is based on practical and historical factors in computer systems:

    Memory Page Size:
        Many systems use 4 KB pages in their memory architecture.
        Aligning chunk sizes to this page size optimizes memory usage.

    CPU and Network Efficiency:
        Small chunks incur higher CPU overhead due to frequent processing.
        Large chunks may cause buffer overflows or delays if the receiver cannot handle them efficiently.

    Error Handling:
        When a transmission error occurs, TCP retransmits only the affected chunk.
        Using a balanced size like 4096 minimizes the retransmission impact while keeping data flow efficient.

4096 bytes strikes a balance between:

    Reducing the number of trips (calls).
    Avoiding excessive memory usage.
    Keeping processing efficient for most systems.


    
### Simple Explanation for Your Grandmother:

Imagine you have a house (your computer) and inside that house, you have a small room (the virtual machine, or Kali Linux in this case). Now, think of the way the house connects to the outside world (the internet).

1. **NAT (Network Address Translation)**: 
   - It's like your house has only one front door to the outside world. The small room (Kali Linux) uses that same door to get out. It doesn’t have its own direct access to the outside world, but it can still use the door of the house. It’s safe, but the room is a bit hidden.
   
2. **Bridged Mode**:
   - This is like the small room having its own door to the outside world. The room (Kali Linux) can go out directly and talk to other houses (computers) on the street, just like your main house can. It’s more like it’s part of the outside world, not hidden.

### Professional Explanation:

**NAT Mode** is a network configuration where your virtual machine shares the same IP address as your host machine (the physical computer running VirtualBox). The VM uses the host’s network connection to access the internet, but it doesn’t appear as a separate device on the network. This means that while the VM can communicate out to the internet, other devices on the network won’t see it directly.

**Bridged Mode** connects the virtual machine to the physical network directly, as if it were another computer on the same network. The VM is given its own unique IP address, allowing it to interact directly with other devices on the network (like printers, other computers, etc.). This makes the VM appear as a separate machine on the network, just like any other device connected to your router.

### Example to Illustrate:

- **NAT Example**: Your virtual machine is like a guest in your house who can ask you (the host machine) to fetch things for them. They can access the internet, but everyone else outside can only see your house (host machine), not the guest.
  
- **Bridged Mode Example**: Your virtual machine is like a guest who has their own phone and can call or talk directly to others. The guest can do whatever they want on the network without needing to go through the host machine.

Let me know if you'd like further details or examples!




Remember that the script reads from stdin and will do so until it receives the end-of-file (EOF) marker. To send EOF, press CTRL-D on your keyboard. But I found on windows, it's CTRL-Z.



python h_code.py -t 10.0.2.15 -p 5555 -l -c

python h_code.py -t 127.0.0.1 -p 5555

'''




import argparse
import socket
import shlex
import subprocess
import sys
import textwrap
import threading


def execute(cmd):
    """
    Execute a shell command and return the output. Executes shell commands on the server-side using subprocess.
    """
    cmd = cmd.strip()
    if not cmd:
        return
    output = subprocess.check_output(shlex.split(cmd), stderr=subprocess.STDOUT)
    return output.decode()


class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # Ensures the socket can be reused immediately after being closed.

    def run(self):
        print(f"Running with target: {self.args.target}, port: {self.args.port}, listen mode: {self.args.listen}")
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        print(f"Connecting to {self.args.target}:{self.args.port}...")
        self.socket.connect((self.args.target, self.args.port))
        print("Connected!")        
        if self.buffer:
            self.socket.send(self.buffer)

        try:
            while True:
                recv_len = 1
                response = ''
                while recv_len:
                    data = self.socket.recv(4096)
                    recv_len = len(data)
                    response += data.decode()
                    if recv_len < 4096:
                        break

                if response:
                    print(response)
                buffer = input('> ')
                buffer += '\n'
                self.socket.send(buffer.encode())
        except KeyboardInterrupt:
            print('User terminated.')
            self.socket.close()
            sys.exit()

    def listen(self):
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)

        while True:
            client_socket, _ = self.socket.accept()
            client_thread = threading.Thread(
                target=self.handle, args=(client_socket,)
            )
            client_thread.start()

    def handle(self, client_socket):
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())
        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096) # 4096 is a standard chunk size in networking, chosen to balance memory usage and transfer efficiency ??? 
                if data:
                    file_buffer += data
                else:
                    break
            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f'Saved file {self.args.upload}'
            client_socket.send(message.encode())
        elif self.args.command:
            cmd_buffer = b''
            while True:
                try:
                    client_socket.send(b'BHP: #> ')
                    while '\n' not in cmd_buffer.decode():
                        cmd_buffer += client_socket.recv(64)
                    response = execute(cmd_buffer.decode())
                    if response:
                        client_socket.send(response.encode())
                    cmd_buffer = b''
                except Exception as e:
                    print(f'Server killed: {e}')
                    self.socket.close() # Closes the server socket to free up resources.
                    sys.exit() # Ends the program using sys.exit() to avoid leaving the process hanging.


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:
            netcat.py -t 192.168.1.108 -p 5555 -l -c # command shell
            netcat.py -t 192.168.1.108 -p 5555 -l -u=mytest.txt # upload to file
            netcat.py -t 192.168.1.108 -p 5555 -l -e="cat /etc/passwd" # execute command
            echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 # echo text to server port 135
            netcat.py -t 192.168.1.108 -p 5555 # connect to server
        ''')
    )
    parser.add_argument('-c', '--command', action='store_true', help='command shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=5555, help='specified port')
    parser.add_argument('-t', '--target', default='192.168.1.203', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')
    
    args = parser.parse_args()
    
    if args.listen:
        buffer = ''
    else:
        buffer = sys.stdin.read()
        # print("Enter your input (Ctrl+D to exit):")
        # buffer = sys.stdin.readline().strip()  # Reads one line of input
    
    nc = NetCat(args, buffer.encode())
    nc.run()
