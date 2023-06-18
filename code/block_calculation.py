import numpy as np
from shapely.geometry import Polygon

# 根据bounding box的四个顶点, 按block_size划分, 构建一个布尔矩阵
def initMaskFromBoundingBox(x_min, x_max, y_min, y_max, block_size):
    """
    Initialize a mask from a bounding box.
    """
    mask = np.zeros((int((x_max - x_min) / block_size), int((y_max - y_min) / block_size)))
    return mask

# 输入bounding box的四个顶点, block_size, polygon的顶点list，将每个block的布尔值计算出来
def calculateMaskFromPolygon(x_min, x_max, y_min, y_max, block_size, polygon):
    mask = initMaskFromBoundingBox(x_min, x_max, y_min, y_max, block_size)
    '''
    对每个mask的小矩形与polygon进行比较, 如果有交集, 则该小矩形为True, 否则为False
    方法为Separating Axis Theorem, 分离轴定理
    '''
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            x1 = x_min + i * block_size
            y1 = y_min + j * block_size
            x2 = x1 + block_size
            y2 = y1 + block_size
            if isRectangleInPolygon(x1, y1, x2, y2, polygon):
                mask[i, j] = 1
    return mask

def isRectangleInPolygon(x1, y1, x2, y2, polygon):
    """
    Judge whether a rectangle intersects with a polygon or not.
    """
    rectangle = Polygon([(x1, y1), (x2, y1), (x2, y2), (x1, y2)])
    return rectangle.intersects(Polygon(polygon))