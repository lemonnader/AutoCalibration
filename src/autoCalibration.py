import cv2
import numpy as np

# 定义两个核	（kernel_Ero用于腐蚀，kernel_Dia用于膨胀）
kernel_Ero = np.ones((3, 1), np.uint8)
kernel_Dia = np.ones((2, 2), np.uint8)

img = cv2.imread("../enhanceEdge.jpg")
copy_img = img.copy()
cv2.imshow("img", copy_img)
# # 原图copy修改尺寸
# copy_img = cv2.resize(copy_img, (1600, 800))
# 灰度值转换
imgGray = cv2.cvtColor(copy_img, cv2.COLOR_BGR2GRAY)
# 高斯滤波去噪
imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 0)
cv2.imshow("filter", imgBlur)

# 阈值处理
ret, thresh = cv2.threshold(imgBlur, 225, 255, cv2.THRESH_BINARY)
cv2.imshow("thresh", thresh)

# 腐蚀
imgEro = cv2.erode(thresh, kernel_Ero, iterations=5)
cv2.imshow("erode", imgEro)

# 膨胀
imgDia = cv2.dilate(imgEro, kernel_Dia, iterations=1)

cv2.imshow("afterHandle", imgDia)

# 轮廓检测
contouts, hie = cv2.findContours(imgDia, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
cnt = contouts

for i in cnt:
    # 坐标赋值
    x, y, w, h = cv2.boundingRect(i)
    # roi位置判断
    if y > 0 and y < 480 and x < 640 and w > 0 and h > 0:
        # 画出轮廓
        cv2.drawContours(copy_img, i, -1, (0, 255, 0), 2)
cv2.imshow("contours",copy_img)

edges = cv2.Canny(imgDia, 50, 150, apertureSize=3)
cv2.imshow("canny",edges)

# image参数表示边缘检测的输出图像，该图像为单通道8位二进制图像。
# rho参数表示参数极径 r 以像素值为单位的分辨率，这里一般使用 1 像素。
# theta参数表示参数极角 \theta 以弧度为单位的分辨率，这里使用 1度。
# threshold参数表示检测一条直线所需最少的曲线交点。
# lines参数表示储存着检测到的直线的参数对 (x_{start}, y_{start}, x_{end}, y_{end}) 的容器，也就是线段两个端点的坐标。
# minLineLength参数表示能组成一条直线的最少点的数量，点数量不足的直线将被抛弃。
# maxLineGap参数表示能被认为在一条直线上的亮点的最大距离。
# print("直线个数："+len(lines[0]))
lines = cv2.HoughLinesP(edges, 1, np.pi/360, 10, minLineLength=10, maxLineGap=500)
# 绘制直线，十条
for each in lines[0: 10]:
    for x1, y1, x2, y2 in each:
        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 2)
cv2.imshow("houghline",img)

cv2.waitKey()
cv2.destroyAllWindows()
