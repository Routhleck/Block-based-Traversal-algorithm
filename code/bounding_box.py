import numpy as np


# 将polygonList的bounding box计算出来，一一对应
def generateBoundingBoxes(polygonList):
    """
    Generate bounding boxes from a list of polygons.
    """
    boundingBoxes = []
    for polygon in polygonList:
        boundingBoxes.append(generateBoundingBox(polygon))
    return boundingBoxes


# 根据一个多边形的顶点list初始化bounding box
def generateBoundingBox(polygon):
    """
    Generate a bounding box from a polygon.
    """
    x_min = np.min(polygon[:, 0])
    x_max = np.max(polygon[:, 0])
    y_min = np.min(polygon[:, 1])
    y_max = np.max(polygon[:, 1])
    return x_min, x_max, y_min, y_max
