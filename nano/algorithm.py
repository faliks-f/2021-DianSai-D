import math


def cal_l(A_T, B_T, theta, flag):
    if flag:
        T = A_T
    elif theta < 10:
        T = B_T
    else:
        if A_T < 0 and B_T < 0:
            T = 2
        elif A_T < 0:
            T = B_T
        elif B_T < 0:
            T = A_T
        else:
            T = (A_T + B_T) / 2

    result = 0.24836 * T * T * 100 - 10.3 / 2 - 4.5
    return result, T


def cal_theta(x_A, x_B, to_zero_flag):
    k = x_A / x_B
    flag = False
    result = math.atan(k)
    result = result / math.pi * 180
    if result > 75:
        k = x_B / x_A
        result = math.atan(k)
        result = 90 - result / math.pi * 180
        flag = True
    if not to_zero_flag:
        return result, flag
    if flag:
        while result < 85:
            x_B = max(x_B - 2, 2)
            print(x_B)
            k = x_B / x_A
            result = math.atan(k)
            result = 90 - result / math.pi * 180
    else:
        while result > 5:
            x_A = max(x_A - 2, 2)
            k = x_A / x_B
            result = math.atan(k)
            result = result / math.pi * 180
    return result, flag

