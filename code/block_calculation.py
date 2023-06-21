import numpy as np
from shapely.geometry import Polygon


# 根据bounding box的四个顶点, 按block_size划分, 构建一个布尔矩阵
def initMaskFromBoundingBox(x_min, x_max, y_min, y_max, block_size):
    """
    Initialize a mask from a bounding box.
    """
    mask = np.zeros((int(np.ceil((x_max - x_min) / block_size[0])),
                     int(np.ceil((y_max - y_min) / block_size[1]))), dtype=np.bool_)
    return mask


# 输入bounding box的四个顶点, block_size, polygon的顶点list，将每个block的布尔值计算出来
def calculateMaskFromPolygon(x_min, x_max, y_min, y_max, block_size, polygon):
    mask = initMaskFromBoundingBox(x_min, x_max, y_min, y_max, block_size)
    """
    对每个mask的小矩形与polygon进行比较, 如果有交集, 则该小矩形为True, 否则为False
    方法为Separating Axis Theorem, 分离轴定理
    """
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            x1 = x_min + i * block_size[0]
            y1 = y_min + j * block_size[1]
            x2 = x1 + block_size[0]
            y2 = y1 + block_size[1]
            if isRectangleInPolygon(x1, y1, x2, y2, polygon):
                mask[i, j] = True
    return mask


def isRectangleInPolygon(x1, y1, x2, y2, polygon):
    """
    判断矩形是否在多边形内部
    """
    rectangle = Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
    return rectangle.intersects(Polygon(polygon))
