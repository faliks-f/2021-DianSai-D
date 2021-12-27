import socket
import time

import cv2
import numpy


class Read:
    __socket = None
    __receive_config = None
    __encode_param = [int(cv2.IMWRITE_JPEG_CHROMA_QUALITY), 100]

    def __init__(self):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def set_read_config(self, ip: str, port: int):
        self.__receive_config = (ip, port)
        self.__socket.connect(self.__receive_config)

    def receive_image(self):
        time = float(self.__recv_size(16))
        length = self.__recv_size(16)
        data = self.__recv_size(int(length))
        data = numpy.frombuffer(data, numpy.uint8)
        image_ = cv2.imdecode(data, cv2.IMREAD_COLOR)
        return image_, time

    def __recv_size(self, count):
        buffer = b''
        while count:
            new_buffer = self.__socket.recv(count)
            if not new_buffer:
                return None
            buffer += new_buffer
            count -= len(new_buffer)
        return buffer

    def __del__(self):
        self.__socket.close()
