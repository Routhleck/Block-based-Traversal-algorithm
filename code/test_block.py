from rasterization import (rasterization_point,
                           rasterization_bounding_box,
                           rasterization_traversal,
                           rasterization_traversal_block)
from draw import drawBooleanMatrixAndPolygons, drawPolygons
from initializer import initPolygonList_custom, initPolygonList_random
import numpy as np
from time import time
import pandas as pd

field_size = (2400, 2400)
polygonList = np.array([[[400, 400], [2000, 400], [1200, 2000]],
                        [[200, 2200], [1200, 200], [2000, 200]],
                        [[400, 200], [2000, 1600], [2000, 2200]]]
                       )

block_size = (200, 200)


# field_size = (20, 20)
# polygonList = np.array([[[0, 0], [20, 0], [0, 20]],])
def testTime(polygonList, field_size, block_size, isDraw=False):
    polygonList = initPolygonList_custom(polygonList)
    if isDraw:
        drawPolygons(polygonList)

    # # 1. 常规的rasterization方法, 对每个像素点, 判断是否在polygon内
    # time1 = time()
    # field_point = rasterization_point(polygonList, field_size)
    # print('point: ', time() - time1)
    #
    # # 2. 使用bounding box的方法, 对每个bounding box, 判断是否在polygon内
    # time2 = time()
    # field_point = rasterization_bounding_box(polygonList, field_size)
    # print('bounding_box: ', time() - time2)

    # 3. 使用traversal方法遍历
    print('Field_size = ', field_size, '\t block_size = ', block_size)
    time3 = time()
    # field_point_1 = rasterization_traversal(polygonList, field_size)
    time3 = time() - time3
    print('traversal: ', time3)

    # 4. 使用block-based traversal方法遍历, 因为JIT是即时编译所以最好在前面就编译好
    field_point_2 = rasterization_traversal_block(polygonList, field_size, block_size)
    time4 = time()
    field_point_2 = rasterization_traversal_block(polygonList, field_size, block_size)
    time4 = time() - time4
    print('block-based traversal: ', time4)
    if isDraw:
        # drawBooleanMatrixAndPolygons(field_point_1, polygonList)
        drawBooleanMatrixAndPolygons(field_point_2, polygonList)


testTime(polygonList, field_size, block_size, True)
