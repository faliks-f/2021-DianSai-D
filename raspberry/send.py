import socket
import time

import cv2
import numpy


class Send:
    __socket = None
    __send_config = None
    __encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 100]
    __connection = None

    def __init__(self):
        pass

    def set_send_config(self, port: int):
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__send_config = ("0.0.0.0", port)
        self.__socket.bind(self.__send_config)
        self.__socket.listen(True)
        self.__connection, client_addr = self.__socket.accept()
        print(client_addr)

    def send_image(self, image):
        result, image_encode = cv2.imencode('.jpg', image, self.__encode_param)
        data = numpy.array(image_encode)
        string_data = data.tostring()
        tick_time = cv2.getTickCount() / cv2.getTickFrequency()
        self.__connection.send(str.encode(str(tick_time).ljust(16)))
        self.__connection.send(str.encode(str(len(string_data)).ljust(16)))
        self.__connection.send(string_data)
        time.sleep(0.01)

    def close(self):
        self.__connection.close()
        self.__socket.close()
        self.__socket = None
        self.__connection = None

    def __del__(self):
        self.__socket.close()
