import socket
import threading
import pandas as panda
import csv

# Constants
PORT = 5050
SERVER = socket.gethostname()
ADDR = (SERVER, PORT)
RBYTE = 1024
FORMAT = 'utf-8'
DISCONNECT = 'quit'
MAX_ENTRIES = 40000

sock_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock_server.bind(ADDR)

columns = ['MemberID','First Name','Last Name','Date of Birth']
db = panda.read_csv('database.csv', index_col='MemberID', parse_dates=['Date of Birth'])

def start():
    sock_server.listen()
    print(f'[LISTENING] on {SERVER}')

    while True:
        conn, addr = sock_server.accept()
        thread = threading.Thread(target=client_handler, args=(conn, addr))
        thread.start()
        print(f'[ACTIVE CONNECTIONS] {threading.active_count() - 1}')

def client_handler(conn, addr):
    print(f'[NEW CONNECTION] {addr} Connected')

    connected = True
    while connected:
        msg_length = conn.recv(RBYTE).decode(FORMAT)
        if msg_length:
            msg_length = int(msg_length)
            msg = conn.recv(msg_length).decode(FORMAT)

            print(f'[CLIENT] {msg}')
            # Database Logic
            split_data = msg.split()
            if split_data[0].lower() == 'find':
                cmd = split_data[0].lower()
                arg = int(split_data[1])
                test = 'FINDING'
                f_return = database(cmd, arg)
                send(conn, f_return)
            elif split_data[0].lower() == 'insert':
                cmd = split_data[0].lower()
                arg = split_data[1:]
                test = 'INSERTING'
                f_return = database(cmd, arg)
                send(conn, f_return)
            elif split_data[0].lower() == 'update':
                cmd = split_data[0].lower()
                test = 'UPDATING'
                send(conn, test)


            if msg == DISCONNECT:
                connected = False
                closing = 'Disconnecting...'
                send(conn, closing)
            print(f'[{addr}] {msg}')

    conn.close()

def send(conn, msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (RBYTE - len(send_length))
    conn.send(send_length)
    conn.send(message)


# database: 'command', 'data'
def database(cmd, arg) -> str:
    # Setting up the database
    records = -1
    with open('database.csv') as datab:
        cr = csv.reader(datab)
        for row in cr:
            records += 1
    print(f'[CURRENT RECORDS] {records}')
    if records == MAX_ENTRIES:
        return 'Database is Full...'
    # Handling the 'Find' option
    if cmd == 'find':
        found = str(db.loc[arg])
        found = found.split()
        f_record = found[12] + " " + found[2] + " " + found[5] + ", " + found[9]
        return f_record
    elif cmd == 'insert':
        arg[2] = panda.to_datetime(arg[2])
        #arg = str(arg)
        slot = records + 2

        temp_db = panda.DataFrame([slot,arg], columns=['MemberID','First Name','Last Name','Date of Birth'])
        db.loc[slot] = temp_db[0]
        db.to_csv('database.csv')
        return 'Successfully Written'
        #temp = str(temp_db)
        #return temp

print('[STARTING] Server is booting')
if __name__ =='__main__':
    start()