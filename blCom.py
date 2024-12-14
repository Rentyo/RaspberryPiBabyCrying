from bluetooth import *
import threading
import detectUseSensor
server_socket= BluetoothSocket(RFCOMM)

port = 1
server_socket.bind(("", port))
server_socket.listen(1)

uuid = "00001101-0000-1000-8000-00805f9b34fb"
advertise_service(server_socket, "SampleServer",
                  service_id=uuid,
                  service_classes=[uuid, SERIAL_PORT_CLASS],
                  profiles=[SERIAL_PORT_PROFILE])

print("소켓 통신")
client_socket, address = server_socket.accept()
print("Accepted connection from ", address)

client_socket.send("bluetooth connected!")

detectUseSensor.Sensor_detect(client_socket)

# while True:
#     send_data = input("입력해주세요 ! : ")
#     client_socket.send(send_data)
#     # data = client_socket.recv(1024)
#     # print("Received: %s" %data)
#     if(send_data=="q"):
#         print("Quit")
#         break
client_socket.close()
server_socket.close()