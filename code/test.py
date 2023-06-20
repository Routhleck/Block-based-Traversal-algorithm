from rasterization import (rasterization_point,
                           rasterization_bounding_box,
                           rasterization_traversal,
                           rasterization_traversal_parallel,
                           rasterization_traversal_block)
from draw import drawBooleanMatrixAndPolygons, drawPolygons
from initializer import initPolygonList_custom, initPolygonList_random
import numpy as np
from time import time
import pandas as pd

field_sizes = [(600, 600), (1200, 1200), (2400, 2400)]
polygonLists = [np.array([[[100, 100], [500, 100], [300, 500]],
                          [[50, 550], [300, 50], [500, 50]],
                          [[100, 50], [500, 400], [500, 550]]]
                         ),
                np.array([[[200, 200], [1000, 200], [600, 1000]],
                          [[100, 1100], [600, 100], [1000, 100]],
                          [[200, 100], [1000, 800], [1000, 1100]]]
                         ),
                np.array([[[400, 400], [2000, 400], [1200, 2000]],
                          [[200, 2200], [1200, 200], [2000, 200]],
                          [[400, 200], [2000, 1600], [2000, 2200]]]
                         )
                ]
block_sizes = [(25, 25), (50, 50), (100, 100), (200, 200), (400, 400)]

df = pd.DataFrame(columns=[
    'field_size',
    'block_size',
    'time_traversal_parallel',
    'time_block_based_traversal',
])


# field_size = (20, 20)
# polygonList = np.array([[[0, 0], [20, 0], [0, 20]],])
def testTime(polygonList, field_size, block_size, isDraw=False):
    polygonList = initPolygonList_custom(polygonList)
    if isDraw:
        drawPolygons(polygonList)

    print('Field_size = ', field_size, '\t block_size = ', block_size)

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
    field_point_1 = rasterization_traversal_block(polygonList, field_size)
    time3 = time()
    field_point_1 = rasterization_traversal_block(polygonList, field_size)
    # 毫秒取2位小数
    time3 = round((time() - time3) * 1000, 2)
    print('traversal: ', time3)

    # 4. 使用block-based traversal方法遍历, 因为JIT是即时编译所以最好在前面就编译好
    field_point_2 = rasterization_traversal_block(polygonList, field_size, block_size)
    time4 = time()
    field_point_2 = rasterization_traversal_block(polygonList, field_size, block_size)
    # 毫秒取2位小数
    time4 = round((time() - time4) * 1000, 2)
    print('block-based traversal: ', time4)
    if isDraw:
        drawBooleanMatrixAndPolygons(field_point_1, polygonList)
        drawBooleanMatrixAndPolygons(field_point_2, polygonList)

    df.loc[len(df)] = [field_size, block_size, time3, time4]


for polygonList, field_size in zip(polygonLists, field_sizes):
    for block_size in block_sizes:
        testTime(polygonList, field_size, block_size, isDraw=False)

df.to_csv('test.csv', index=False)
