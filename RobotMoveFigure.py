import socket
from _socket import SHUT_RDWR

ROBOT_HOST = "192.168.0.103"  # IP адрес робота на ктоторый мы отсылаем сообщение
ROBOT_PORT = 3000  # Порт по которому передаётся сообщение
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Создаём сокет передачи и подключаемся
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)  # Защита от проблем при запуске
s.bind((ROBOT_HOST, ROBOT_PORT))
s.listen(10)

try:
    connection, _ = s.accept()
    while True:
        '''
        x,y,
        1(grab)
        2(place)
        3(pallet)
        '''
        #words = [chr(int(input())) , chr(int(input())), chr(int(input()))]
        #connection.send((words[0] + words[1] + words[2]).encode('utf8'))  # Передаём информацию

        for i in range(3):
            for j in range(4):
                k = j*2 if i%2==0 else j*2+1
                connection.send((chr(k) + chr(i) + chr(3)).encode('utf8'))  # Передаём информацию
    connection.close()
finally:
    s.shutdown(SHUT_RDWR)
    s.close()  # Закрываем сокет







