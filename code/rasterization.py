from block_calculation import calculateMaskFromPolygon
from bounding_box import generateBoundingBoxes
from initializer import initPolygonFromVertexes, initRandomPolygon
from traverse_polygon import traverseMask, traverseSingle, isPointInPolygon, traverseAllblock

import numpy as np


def rasterization_point(polygonList, field_size):
    """
    常规的rasterization方法, 对每个像素点, 判断是否在polygon内
    """
    # 初始化field
    field = np.zeros(field_size, dtype=np.bool_)
    # 取出每个polygon的顶点list
    for polygon in polygonList:
        for i in range(field_size[0]):
            for j in range(field_size[1]):
                if isPointInPolygon((i, j), polygon):
                    field[i, j] = True
    return field


def rasterization_bounding_box(polygonList, field_size):
    """
    使用bounding box的方法, 对每个bounding box, 判断是否在polygon内
    """
    # 初始化field
    field = np.zeros(field_size, dtype=np.bool_)
    # 取出每个polygon的bounding box
    boundingBoxes = generateBoundingBoxes(polygonList)
    for boundingBox_index, polygon in enumerate(polygonList):
        for j in range(boundingBoxes[boundingBox_index][0], boundingBoxes[boundingBox_index][1]):
            for i in range(boundingBoxes[boundingBox_index][2], boundingBoxes[boundingBox_index][3]):
                if isPointInPolygon((i, j), polygon):
                    field[i, j] = True
    return field


def rasterization_traversal(polygonList, field_size):
    """
    使用traversal方法遍历
    """
    # 初始化field
    field = np.zeros(field_size, dtype=np.bool_)
    # 取出每个polygon的bounding box
    boundingBoxes = generateBoundingBoxes(polygonList)

    # 遍历每个polygon
    for boundingBox_index, polygon in enumerate(polygonList):
        field = traverseSingle((boundingBoxes[boundingBox_index][0],
                                boundingBoxes[boundingBox_index][2]),
                               polygon,
                               field,
                               boundingBoxes[boundingBox_index][0],
                               boundingBoxes[boundingBox_index][2],
                               boundingBoxes[boundingBox_index][1],
                               boundingBoxes[boundingBox_index][3])

    return field


def rasterization_traversal_parallel(polygonList, field_size, block_size):
    """
    使用traversal方法遍历
    """
    # 初始化field
    field = np.zeros(field_size, dtype=np.bool_)
    # 取出每个polygon的bounding box
    boundingBoxes = generateBoundingBoxes(polygonList)

    # 遍历每个polygon
    for boundingBox_index, polygon in enumerate(polygonList):
        mask = calculateMaskFromPolygon(boundingBoxes[boundingBox_index][0],
                                        boundingBoxes[boundingBox_index][1],
                                        boundingBoxes[boundingBox_index][2],
                                        boundingBoxes[boundingBox_index][3],
                                        block_size,
                                        polygon)
        field = traverseAllblock(mask,
                                 block_size,
                                 field,
                                 boundingBoxes[boundingBox_index][0],
                                 boundingBoxes[boundingBox_index][2],
                                 boundingBoxes[boundingBox_index][1],
                                 boundingBoxes[boundingBox_index][3],
                                 polygon)

    return field


def rasterization_traversal_block(polygonList, field_size, block_size=(32, 32)):
    """
    使用block-based traversal方法遍历
    """
    # 初始化field
    field = np.zeros(field_size, dtype=np.bool_)
    # 取出每个polygon的bounding box
    boundingBoxes = generateBoundingBoxes(polygonList)

    # 遍历每个polygon
    for boundingBox_index, polygon in enumerate(polygonList):
        mask = calculateMaskFromPolygon(boundingBoxes[boundingBox_index][0],
                                        boundingBoxes[boundingBox_index][1],
                                        boundingBoxes[boundingBox_index][2],
                                        boundingBoxes[boundingBox_index][3],
                                        block_size,
                                        polygon)
        field = traverseMask(mask,
                             block_size,
                             field,
                             boundingBoxes[boundingBox_index][0],
                             boundingBoxes[boundingBox_index][2],
                             boundingBoxes[boundingBox_index][1],
                             boundingBoxes[boundingBox_index][3],
                             polygon)
    return field
