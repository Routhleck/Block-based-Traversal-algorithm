from rasterization import (rasterization_point,
                           rasterization_bounding_box,
                           rasterization_traversal,
                           rasterization_traversal_block)
from draw import drawBooleanMatrixAndPolygons, drawPolygons
from initializer import initPolygonList_custom, initPolygonList_random
import numpy as np

field_size = (600, 600)
polygonList = np.array([[[100, 500], [400, 400], [500, 250]],
                        [[100, 100], [400, 200], [500, 50]],]
                       )

polygonList = initPolygonList_custom(polygonList)

drawPolygons(polygonList)
# 1. 常规的rasterization方法, 对每个像素点, 判断是否在polygon内
# field_point = rasterization_point(polygonList, field_size)
# 2. 使用bounding box的方法, 对每个bounding box, 判断是否在polygon内
# field_point = rasterization_bounding_box(polygonList, field_size)
# 3. 使用traversal方法遍历
field_point = rasterization_traversal(polygonList, field_size)
drawBooleanMatrixAndPolygons(field_point, polygonList)
