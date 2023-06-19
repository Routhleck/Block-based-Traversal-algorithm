import numpy as np
from shapely.geometry import Polygon, Point
from numba import jit, njit

"""
输入mask, 布尔矩阵field, bounding box的四个顶点, polygon的顶点list, 
只计算mask中为True的部分, 
针对mask所对应的block中的每个值, 使用traversal算法, 修改field中的值
traversal算法: 首先找到polygon在该block中离左上方最近的顶点(注意优先判断离上方最近, 其次是离左侧最近),
然后从该点开始, 向右遍历, 直到出block边界或者该点不在polygon内, 
就往下一个单位, 判断是否在polygon内, 然后开始向左遍历, 直到出block边界或者该点不在polygon内, 就往下一个单位, 
在重复上述过程中, 遍历的方向会左右改变, 直到遍历到最后一行的出block边界或者该点不在polygon内
"""


def traverseMask(mask, block_size, field, x_min, y_min, x_max, y_max, polygon):
    """
    Traverse a mask and modify a field.
    """
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
            if mask[i, j]:
                block_start = [x_min + i * block_size[0], y_min + j * block_size[1]]
                field = traverseBlock(block_start, block_size, polygon, field, x_min, y_min, x_max, y_max)

    return field

def traverseAllblock(mask, block_size, field, x_min, y_min, x_max, y_max, polygon):
    for i in range(mask.shape[0]):
        for j in range(mask.shape[1]):
                block_start = [x_min + i * block_size[0], y_min + j * block_size[1]]
                field = traverseBlock(block_start, block_size, polygon, field, x_min, y_min, x_max, y_max)

    return field


@jit(nopython=True, parallel=True)
def traverseBlock(block_start, block_size, polygon, field, x_min, y_min, x_max, y_max):
    # 找到start点
    cursor = findStartPointJit(block_start, block_size, polygon)
    if cursor is None:
        return field
    # 从start点开始遍历
    # 首先向右遍历
    shouldStop = False
    step = 1
    colStartInPolygon = True
    while not shouldStop:
        if colStartInPolygon:
            if not isPointInPolygonJit((cursor[1], cursor[0]), polygon) \
                    or cursor[0] < x_min \
                    or cursor[0] > x_max:
                step = -step
                cursor[1] += 1
                if cursor[1] > y_max:
                    shouldStop = True
                colStartInPolygon = False
            else:
                field[cursor[1], cursor[0]] = True
                cursor[0] += step
        else:
            if not isPointInPolygonJit((cursor[1], cursor[0]), polygon):
                cursor[0] += step
                if cursor[0] < x_min or cursor[0] > x_max:
                    shouldStop = True
            else:
                colStartInPolygon = True

    return field


def traverseSingle(start, polygon, field, x_min, y_min, x_max, y_max):
    cursor = findStartPoint(start, field.shape, polygon)
    step = 1
    shouldStop = False
    colStartInPolygon = True
    while not shouldStop:
        if colStartInPolygon:
            if not isPointInPolygon((cursor[1], cursor[0]), polygon) \
                    or cursor[0] < x_min \
                    or cursor[0] > x_max:
                step = -step
                cursor[1] += 1
                if cursor[1] > y_max:
                    shouldStop = True
                colStartInPolygon = False
            else:
                field[cursor[1], cursor[0]] = True
                cursor[0] += step
        else:
            if not isPointInPolygon((cursor[1], cursor[0]), polygon):
                cursor[0] += step
                if cursor[0] < x_min or cursor[0] > x_max:
                    shouldStop = True
            else:
                colStartInPolygon = True

    return field


def findStartPoint(block_start, block_size, polygon):
    # 找到polygon中离block_start最近的点
    # 优先判断离上方最近, 其次是离左侧最近
    for i in range(block_size[0]):
        for j in range(block_size[1]):
            if isPointInPolygon((block_start[1] + i, block_start[0] + j), polygon):
                return [block_start[0] + j, block_start[1] + i]


@jit(nopython=True)
def findStartPointJit(block_start, block_size, polygon):
    # 找到polygon中离block_start最近的点
    # 优先判断离上方最近, 其次是离左侧最近
    for i in range(block_size[0]):
        for j in range(block_size[1]):
            if isPointInPolygonJit((block_start[1] + i, block_start[0] + j), polygon):
                return [block_start[0] + j, block_start[1] + i]


def isPointInPolygon(point, polygon):
    # 使用shapely的方法判断点是否在polygon内
    polygon = Polygon(polygon)
    return polygon.contains(Point(point[1], point[0]))


@njit
def isPointInPolygonJit(point, polygon):
    y, x = point
    n = len(polygon)
    inside = False
    p1x, p1y = polygon[0]
    for i in range(n + 1):
        p2x, p2y = polygon[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside
