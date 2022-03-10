import bluetooth
import picar_4wd as fc
import signal
import sys
#Interrupt handler
def signal_handler(signal, frame):
    fc.stop()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)


power_val = 10

hostMACAddress = "B8:27:EB:34:24:F0" # The address of Raspberry PI Bluetooth adapter on the server. The server might have multiple Bluetooth adapters.
port = 0
backlog = 1
size = 1024
s = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
s.bind((hostMACAddress, port))
s.listen(backlog)
print("listening on port ", port)
try:
    client, clientInfo = s.accept()
    while 1:   
        data = client.recv(size)
        if data:
            key = data.decode('utf-8')
            print(key)
            if key=='w':
                fc.forward(power_val)
            elif key=='a':
                fc.turn_left(power_val)
            elif key=='s':
                fc.backward(power_val)
            elif key=='d':
                fc.turn_right(power_val)
            else:
                fc.stop()
            if key=='q':
                print("quit")  
                break  

            client.send(data) # Echo back to client
except Exception as E:
    print(E) 
    print("Closing socket")
    fc.stop()
    client.close()
    s.close()

