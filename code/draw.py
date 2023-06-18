import matplotlib.pyplot as plt
import numpy as np

# 根据布尔矩阵绘制整个画面
def drawBooleanMatrix(booleanMatrix):
    plt.imshow(booleanMatrix, cmap='gray')
    plt.show()

# 根据顶点绘制多边形
def drawPolygon(polygon):
    plt.plot(polygon[:, 0], polygon[:, 1])
    plt.show()

# 将两张图片叠加
def drawBooleanMatrixAndPolygon(booleanMatrix, polygon):
    plt.imshow(booleanMatrix, cmap='gray')
    plt.plot(polygon[:, 0], polygon[:, 1])
    plt.show()
    