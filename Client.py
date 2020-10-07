import socket
import random


# Constants
PORT = 5050
SERVER = socket.gethostname()
ADDR = (SERVER, PORT)
RBYTE = 1024
FORMAT = 'utf-8'
DISCONNECT = 'quit'
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


def main():
    client.connect(ADDR)
    connected = True
    while connected:
        user_message = input(' -> ')
        
        # Disconnect handling
        if user_message == DISCONNECT:
            connected = False
            response = send_recv(user_message)
            print(f'[SERVER] {response}')

        server_message = send_recv(user_message)
        print(f'[SERVER]\n {server_message}')

        
    
    client.close()


def send_recv(msg) -> str:
    # Handling the sending of the message to the server.
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (RBYTE - len(send_length))
    client.send(send_length)
    client.send(message)

    # Handling recieving from the server.
    r_msg_len = client.recv(RBYTE).decode(FORMAT)
    r_msg_len = int(r_msg_len)
    r_msg = client.recv(r_msg_len).decode(FORMAT)
    return r_msg

# This function returns a string, of which is randomly generated from the 'names.txt' file, and creates a random entry for the "database".
def name_maker() -> str:
    names = []
    retName = ""
    with open("names.txt") as fileName:
        for name in fileName:
            name=name.strip()
            names.append(name)
    first_name = names[random.randint(0, len(names) - 1)]
    last_name = names[random.randint(0, len(names) - 1)]
    DoB = ""
    day = random.randint(1, 28)
    month = random.randint(1, 12)
    year = random.randint(1970, 2020)
    DoB = str(day) + "/" + str(month) + "/" + str(year)
    retName = first_name + " " + last_name + " " + DoB
    return retName


if __name__ == '__main__':
    main()
