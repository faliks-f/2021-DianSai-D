from raspberry.send import Send
import cv2
import _thread
import time
from raspberry.fix_distortion import fix_distortion

image = None


def send_image_thread(thread_name, sender, port):
    while True:
        try:
            sender.set_send_config(port)
            while True:
                if image is None:
                    continue
                image_copy = image.copy()
                sender.send_image(image_copy)
        except Exception as e:
            print(e)
            sender.close()


if __name__ == '__main__':
    sender = Send()
    capture = cv2.VideoCapture(0)
    print(capture.isOpened())
    _thread.start_new_thread(send_image_thread, (1, sender, 8001))
    cv2.namedWindow("MainWindow", cv2.WINDOW_AUTOSIZE)
    cv2.moveWindow("MainWindow", 0, 0)
    while True:
        _, image_temp = capture.read()
        image = fix_distortion(image_temp, 3)
        cv2.imshow("MainWindow", image)
        cv2.waitKey(1)
