import cv2
import numpy as np

path = "../images/"
y_const = 200
b_threshold = 5
# img_res = cv2.imread(path+'mode2.jpg')
img_res = cv2.imread("../enhanceEdge.jpg")
cv2.imshow("res", img_res)

img_gray = cv2.cvtColor(img_res, cv2.COLOR_BGR2GRAY)
cv2.imwrite(path+"gray.jpg", img_gray)
cv2.imshow("gray", img_gray)

Imax = np.max(img_gray)
Imin = np.min(img_gray)
print("原图亮度范围:", Imax, Imin)
MAX = 255
MIN = 0
gray_contrast = (img_gray - Imin) / (Imax - Imin) * (MAX - MIN) + MIN
cv2.imshow("contrast", gray_contrast.astype("uint8"))
print("对比度增强之后亮度范围:", np.max(gray_contrast), np.min(gray_contrast))

edges = cv2.Canny(img_gray, 30, 100)

lines = cv2.HoughLinesP(edges, 1, np.pi/360, 110, minLineLength=30, maxLineGap=100)
# # 绘制直线，十条
# for each in lines[0: 10]:
#     for x1, y1, x2, y2 in each:
#         cv2.line(img_res, (x1, y1), (x2, y2), (255, 0, 0), 2)
print("直线个数:", len(lines))
#斜率
k_sum = 0
realLines_k = lines
for i in range(len(lines)):
    for x1, y1, x2, y2 in lines[i]:
        tmp_k = (y2 - y1)/(x2 - x1)
        if -0.1 < tmp_k < 0.1:
            realLines_k = np.delete(realLines_k, [i], axis=0)
        else:
            cv2.line(img_res, (x1, y1), (x2, y2), (0, 255, 0), 1)
            cv2.imwrite(path + "lines.jpg", img_res)
            print(tmp_k)
            k_sum += tmp_k
print("剩余直线个数", len(realLines_k))
k = k_sum/len(realLines_k)
print("斜率：", k)

print("去除横线： ", realLines_k)
realLines_b= realLines_k
b = []
print("截距：")
for i in range(len(realLines_k)):
    for x1, y1, x2, y2 in realLines_k[i]:
        tmp_b = abs(y1 - k*x1)
        print(tmp_b)
        b.append(tmp_b)
b.sort()
print("截距个数: ", len(b))
#print("截距们：", b)

realB = list(b)
for i in range(len(b)):
    if i >= 1 and b[i] - b[i-1] < b_threshold:
        realB.remove(b[i])
print("排除相距太近的直线之后的截距个数: ", len(realB))
print("截距们：", realB)

T = []
Points = []
for i in range(len(realB)):
    if i > 0:
        # 相邻截距的差值是半个周期
        T_tmp = realB[i] - realB[i-1]
        T.append(T_tmp * 2)
        # 横轴两个交界点的中点，可能是黑条纹的中间，也可能是白条纹的中间
        point_x = (realB[i] + realB[i-1])/2


cv2.imshow('edges', edges)
cv2.imshow('lines', img_res)
cv2.waitKey()
cv2.destroyAllWindows()
