import socket
import picar_4wd as fc
import signal 

HOST = "192.168.10.20" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)


def signal_handler(signal, frame):
    fc.stop()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


STANDARD_SUFFIX = "\r\n"
SPEED = 15
direction = ""


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    try:
        client, clientInfo = s.accept()
        while 1:
            data = client.recv(1024)      # receive 1024 Bytes of message in binary format

            if data != b"":

                print(data)
                if data == b"87":
                    # w, up
                    fc.forward(SPEED)
                    direction = "Forward"
                elif data == b"83":
                    # s, down
                    fc.backward(SPEED)
                    direction = "Backward"
                elif data == b"65":
                    # a, left
                    fc.turn_left(SPEED)
                    direction = "LEFT"
                elif data == b"68":
                    # d, right
                    fc.turn_right(SPEED)
                    direction = "Right"
                elif data == b"STOP":
                    fc.stop()
                    direction = ""

                else:
                    client.sendall(data) # Echo back to client
    except: 
        print("Closing socket")
        client.close()
        s.close()    
