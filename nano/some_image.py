import cv2
import numpy as np


def get_button_image():
    img = np.zeros((200, 1280, 3), np.uint8)
    img.fill(255)
    return img


def get_ellipse():
    img = np.zeros((600, 1280, 3), np.uint8)
    img.fill(255)
    cv2.line(img, (440, 150), (840, 150), (0, 0, 0), 1)
    cv2.line(img, (840, 150), (840, 500), (0, 0, 0), 1)
    cv2.line(img, (840, 150), (640, int(150 + 400 * (3 ** 0.5) / 2)), (0, 0, 0), 1)
    cv2.line(img, (840, 150), (int(840 - 400 * (3 ** 0.5) / 2), 350), (0, 0, 0), 1)
    cv2.putText(img, "A", (420, 140), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
    cv2.putText(img, "B", (830, 530), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
    cv2.putText(img, "30", (int(840 - 400 * (3 ** 0.5) / 2) - 50, 370), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
    cv2.putText(img, "60", (620, int(50 + 400 * (3 ** 0.5) / 2) + 130), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 1)
    # cv2.imshow("1", img)
    # cv2.waitKey(0)
    return img


if __name__ == '__main__':
    get_ellipse()
