import socket
import struct


class Client:
    def __init__(self, server_port):
        try:
            self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        except socket.error:
            print("Error creating client's socket")
        server_address = socket.gethostbyname(socket.gethostname())
        self.__server_address = (server_address, server_port)
        self.__socket.connect(self.__server_address)
        self.__turn = self.get_turn()

    def send(self, row: int, column: int, winner: int):
        try:
            self.__socket.send(struct.pack('!H', row))
            self.__socket.send(struct.pack('!H', column))
            self.__socket.send(struct.pack('!H', winner))
        except socket.error as error:
            print("Error sending data: ", error)

    def receive(self) -> tuple[int, int, int]:
        row, column, winner = 0, 0, 0
        try:
            data = self.__socket.recv(2)
            row = struct.unpack('!H', data)[0]
            data = self.__socket.recv(2)
            column = struct.unpack('!H', data)[0]
            data = self.__socket.recv(2)
            winner = struct.unpack('!H', data)[0]
        except socket.error as error:
            print("Error receiving data: ", error)

        return row, column, winner

    def get_turn(self) -> int:
        data = self.__socket.recv(2)
        return struct.unpack('!H', data)[0]

    @property
    def turn(self):
        return self.__turn