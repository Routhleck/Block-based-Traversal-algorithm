from rasterization import (rasterization_point,
                           rasterization_bounding_box,
                           rasterization_traversal,
                           rasterization_traversal_block)
from draw import drawBooleanMatrixAndPolygons, drawPolygons
from initializer import initPolygonList_custom, initPolygonList_random
import numpy as np
from time import time

field_size = (600, 600)
polygonList = np.array([[[100, 500], [400, 400], [500, 250]],
                        [[100, 100], [400, 200], [500, 50]],]
                       )
block_size = (100, 100)
# field_size = (20, 20)
# polygonList = np.array([[[0, 0], [20, 0], [0, 20]],])

polygonList = initPolygonList_custom(polygonList)

drawPolygons(polygonList)
# 1. 常规的rasterization方法, 对每个像素点, 判断是否在polygon内
time1 = time()
field_point = rasterization_point(polygonList, field_size)
print('point: ', time() - time1)

# 2. 使用bounding box的方法, 对每个bounding box, 判断是否在polygon内
time2 = time()
field_point = rasterization_bounding_box(polygonList, field_size)
print('bounding_box: ', time() - time2)

# 3. 使用traversal方法遍历
time3 = time()
field_point = rasterization_traversal(polygonList, field_size)
print('traversal: ', time() - time3)

# 4. 使用block-based traversal方法遍历
time4 = time()
field_point = rasterization_traversal_block(polygonList, field_size, block_size)
print('block-based traversal: ', time() - time4)

drawBooleanMatrixAndPolygons(field_point, polygonList)
