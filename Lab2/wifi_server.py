import socket
import picar_4wd as fc
import signal

HOST = "192.168.10.20" # IP address of your Raspberry PI
PORT = 65432          # Port to listen on (non-privileged ports are > 1023)

from gpiozero import CPUTemperature



def signal_handler(signal, frame):
    fc.stop()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


STANDARD_SUFFIX = "\r\n"
SPEED = 15
direction = ""
ack = ""


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    speed = 0

    try:
        client, clientInfo = s.accept()
        while 1:
            data_b = client.recv(1024)      # receive 1024 Bytes of message in binary format

            if data_b != b"":
                data = data_b.decode('utf-8')
                cpu = CPUTemperature().temperature


                if data == "87":
                    # w, up
                    fc.forward(SPEED)
                    direction = "Forward"
                    speed = SPEED
                elif data == "83":
                    # s, down
                    fc.backward(SPEED)
                    direction = "Backward"
                    speed = SPEED
                elif data == "65":
                    # a, left
                    fc.turn_left(SPEED)
                    direction = "LEFT"
                    speed = SPEED
                elif data == "68":
                    # d, right
                    fc.turn_right(SPEED)
                    direction = "Right"
                    speed = SPEED
                elif data == "STOP":
                    fc.stop()
                    direction = "Stopped"
                    speed = 0

                if len(data) > 2 and data[:3] == "ACK":
                    ack = data[3:]

                data = ",".join([data, ack, direction, str(speed), str(cpu) ])
                print(data)
                print(direction)

                client.sendall(data.encode('ascii'))

    except:
        print("Closing socket")
        client.close()
        s.close()
