import cv2
import imutils
import numpy as np

black_min = np.array([0, 0, 0])
black_max = np.array([180, 255, 50])


class Search:

    def __init__(self, name):
        self.name = name
        self.count = 0
        self.max_count = 10
        self.left_x = 640
        self.right_x = 0
        self.record_point = None
        self.start_t = None
        self.end_t = None
        self.t = 0
        self.direction = "left"
        self.T = None
        self.deltaX = None
        self.start_flag = False
        self.time_list = []

    def reset(self):
        self.count = 0
        self.max_count = 10
        self.left_x = 640
        self.right_x = 0
        self.record_point = None
        self.start_t = None
        self.end_t = None
        self.t = 0
        self.direction = "left"
        self.T = None
        self.deltaX = None
        self.start_flag = False
        self.time_list = []

    def start_measure(self):
        self.start_flag = True

    def get_T_and_deltaX(self):
        return self.T, self.deltaX

    def calculate_T_and_deltaX(self):
        time_list = sorted(self.time_list)
        time_list = time_list[2:-2]
        count = 0
        for time in time_list:
            if time < 1.5:
                count += 1
        if count == 6:
            self.T = -1
        else:
            self.T = sum(time_list[count:]) / max(1, (self.max_count - 4 - count))
        self.deltaX = self.right_x - self.left_x
        self.start_flag = False

    def analysis(self, point, tick_time):
        x = point[0]
        if self.record_point is None:
            self.record_point = point
            return
        record_x = self.record_point[0]
        if x < record_x:
            if self.direction == "right":
                self.direction = "left"
                if self.count == 0:
                    self.start_t = self.t
                else:
                    self.time_list.append(self.t - self.start_t)
                    self.start_t = self.t
                if self.count == self.max_count:
                    self.calculate_T_and_deltaX()
                self.count += 1
            if self.left_x > x:
                if self.count < 5:
                    self.left_x = x
        if x > record_x:
            if self.direction == "left":
                self.direction = "right"
            if self.right_x < x:
                if self.count < 5:
                    self.right_x = x
        self.record_point = point
        self.t = tick_time

    def search_black(self, image, tick_time):
        hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, black_min, black_max)
        cnts = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
        c = None
        for c_ in cnts:
            if 1500 > cv2.contourArea(c_) > 10:
                bounding_box = cv2.boundingRect(c_)
                if bounding_box[0] < 5 and bounding_box[1] < 5:
                    continue
                if bounding_box[0] < 5 and bounding_box[1] + bounding_box[3] > 475:
                    continue
                if bounding_box[0] + bounding_box[2] > 635 and bounding_box[1] < 5:
                    continue
                if bounding_box[0] + bounding_box[2] > 635 and bounding_box[1] + bounding_box[3] > 475:
                    continue
                # print(bounding_box)
                if bounding_box[2] < bounding_box[3] * 1.1:
                    c = c_
                    break
        if c is None:
            return
        bounding_box = cv2.boundingRect(c)
        cv2.rectangle(image, (bounding_box[0], bounding_box[1]),
                      (bounding_box[0] + bounding_box[2], bounding_box[1] + bounding_box[3]),
                      (0, 0, 255), 2)
        M = cv2.moments(c)
        if M["m00"] == 0 or M["m00"] == 0:
            return
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        message = "Center(" + str(cX) + "," + str(cY) + ")"
        cv2.putText(image, message, (bounding_box[0] - 20, bounding_box[1] - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)
        if self.start_flag:
            self.analysis((cX, cY), tick_time)
