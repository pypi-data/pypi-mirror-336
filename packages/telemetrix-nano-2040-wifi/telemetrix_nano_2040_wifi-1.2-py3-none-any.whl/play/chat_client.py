import socket
import time


class ChatClient:
    def __init__(self, ip_address, ip_port):
        self.ip_address = ip_address
        self.ip_port = ip_port
        self.message_length = None
        print('Establishing IP connection...')
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            # self.sock.settimeout(8)
            self.sock.connect((self.ip_address, self.ip_port))
            time.sleep(1)
        except socket.timeout:
            print(f'Could not establish a connection to {self.ip_address}:{self.ip_port}')
            try:
                self.sock.shutdown(socket.SHUT_RDWR)
                self.sock.close()
            except Exception:
                pass
            raise

        print(f'Successfully connected to: {self.ip_address}:{self.ip_port}')

    def send_message(self, message):
        self.message_length = len(message)
        # message = message.encode()
        for z in range(self.message_length):
            self.sock.send(message[z].encode())
        # self.sock.flush()
        time.sleep(.01)

    def receive_message(self):
        msg = []
        for ii in range(self.message_length):
            reply = self.sock.recv(1)
            reply = reply.decode()
            msg.append(reply)
        print("".join(msg))


cc = ChatClient('192.168.2.174', 31335)

while True:
    for i in range(3):
        cc.send_message(f'hello{i}\n')
        # time.sleep(.2)
        cc.receive_message()
        # time.sleep(.2)
    time.sleep(.01)
