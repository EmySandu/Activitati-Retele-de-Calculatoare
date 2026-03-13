import socket

HOST = "127.0.0.1"
PORT = 3333
BUFFER_SIZE = 1024


# Meniu de comenzi pentru client (Stiu ca nu era necesar, dar am vrut sa fie mai user-friendly)
MENU = """
==================== MENIU COMENZI ====================
ADD <key> <value>         - adauga (sau suprascrie) perechea key=value
GET <key>                 - returneaza valoarea cheii (DATA <value>)
REMOVE <key>              - sterge cheia si valoarea asociata
LIST                      - afiseaza toate datele: DATA|k1=v1,k2=v2
COUNT                     - afiseaza numarul de elemente: DATA <count>
CLEAR                     - sterge tot dictionarul: OK all data deleted
UPDATE <key> <new_value>  - actualizeaza valoarea unei chei existente
POP <key>                 - returneaza valoarea si apoi sterge cheia
QUIT                      - inchide sesiunea curenta cu serverul
exit                      - alias local pentru QUIT
help                      - afiseaza din nou acest meniu
=======================================================
""".strip()

def receive_full_message(sock):
    try:
        data = sock.recv(BUFFER_SIZE)
        if not data:
            return None

        string_data = data.decode('utf-8').strip()
        first_space = string_data.find(' ')

        if first_space == -1 or not string_data[:first_space].isdigit():
            return "Invalid response format from server"

        message_length = int(string_data[:first_space])
        full_data = string_data[first_space + 1:]
        remaining = message_length - len(full_data)

        while remaining > 0:
            data = sock.recv(BUFFER_SIZE)
            if not data:
                return None
            full_data += data.decode('utf-8')
            remaining -= len(data)

        return full_data
    except Exception as e:
        return f"Error: {e}"

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        print("Connected to server.")
        print(MENU)

        while True:
            command = input('client> ').strip()
            
            if not command:
                continue

            if command.lower() == 'help':
                print(MENU)
                continue

            if command.lower() == 'exit':
                command = 'QUIT'
            
            s.sendall(command.encode('utf-8'))
            response = receive_full_message(s)
            print(f"Server response: {response}")

            if command.upper() == 'QUIT':
                break

if __name__ == "__main__":
    main()
