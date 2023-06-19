import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np


# 根据多个多边形的顶点列表绘制多边形
def drawPolygons(polygonList):
    fig, ax = plt.subplots()
    for polygon in polygonList:
        polygon_patch = patches.Polygon(polygon, fill=False, edgecolor='red')
        ax.add_patch(polygon_patch)
    ax.autoscale_view()  # 自动调整视图以适应所有的多边形
    plt.show()


# 根据布尔矩阵和多个多边形的顶点列表绘制图像
def drawBooleanMatrixAndPolygons(booleanMatrix, polygonList):
    fig, ax = plt.subplots()
    ax.imshow(booleanMatrix, cmap='gray', origin='lower')
    for polygon in polygonList:
        polygon_patch = patches.Polygon(polygon, fill=False, edgecolor='red')
        ax.add_patch(polygon_patch)
    ax.autoscale_view()  # 自动调整视图以适应所有的多边形
    plt.show()
