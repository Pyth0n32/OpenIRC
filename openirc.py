import socket
import threading

class IRCClient:
    def __init__(self, nickname, server, port=6667):
        self.nickname = nickname
        self.server = server
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((server, port))
        self.send_message(f"USER {nickname} 0 * :{nickname}")
        self.send_message(f"NICK {nickname}")
        self.receive_thread = threading.Thread(target=self.receive_messages)
        self.receive_thread.start()

    def send_message(self, message):
        self.socket.send(f"{message}\r\n".encode())

    def receive_messages(self):
        while True:
            data = self.socket.recv(4096).decode("utf-8")
            if data:
                print(data)

    def send_chat_message(self, channel, message):
        self.send_message(f"PRIVMSG {channel} :{message}")

    def join_channel(self, channel):
        self.send_message(f"JOIN {channel}")

    def quit(self, message="Leaving"):
        self.send_message(f"QUIT :{message}")
        self.socket.close()

if __name__ == "__main__":
    nickname = input("Enter nickname: ")
    server = input("Enter server: ")
    port = int(input("Enter port (default is 6667): ") or 6667)

    client = IRCClient(nickname, server, port)

    while True:
        command = input("> ")
        if command.startswith("/join"):
            _, channel = command.split(" ", 1)
            client.join_channel(channel)
        elif command.startswith("/quit"):
            client.quit()
            break
        else:
            client.send_chat_message("#general", command)
