import cv2
import numpy as np

""" feed in an image and the number of device, which is labeled on each camera, 
    and will give back an image without distortion 
    @param frame: a matrix of an image
    @param device_no: the number of the camera
"""


def fix_distortion(frame, device_no):
    device_no -= device_no

    fx = [6.578781710332930, 6.431743611548535, 6.409046400258181, 6.500001462966193]
    cx = [2.981204852712382, 3.039608565667805, 3.426210923032348, 3.024162792945335]
    fy = [6.588587690056696, 6.437363809673791, 6.403594784501500, 6.478190483957260]
    cy = [2.401280022282228, 2.550141765531978, 2.287476935350434, 2.448082822612350]
    k1 = [-0.370595149191223, -0.368825345939742, -0.369629516183312, -0.387547322162571]
    k2 = [0.132122404566604, 0.122915488139599, 0.142791297607277, 0.168604252708103]
    p1 = [0, 0, 0, 0]
    p2 = [0, 0, 0, 0]
    k3 = [0, 0, 0, 0]

    # transformation matrix of camera coordinate to pixel coordinate
    k = np.array([
        [fx[device_no] * 100, 0, cx[device_no] * 100],
        [0, fy[device_no] * 100, cy[device_no] * 100],
        [0, 0, 1]
    ])
    # distortion coefficient
    d = np.array([k1[device_no], k2[device_no], p1[device_no], p2[device_no], k3[device_no]])
    h, w = frame.shape[:2]
    # calculate
    map_x, map_y = cv2.initUndistortRectifyMap(k, d, None, k, (w, h), 5)
    # output
    return cv2.remap(frame, map_x, map_y, cv2.INTER_LINEAR)
