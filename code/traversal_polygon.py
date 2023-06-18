import numpy as np
from shapely.geometry import Polygon

"""
输入mask, 布尔矩阵field, bounding box的四个顶点, polygon的顶点list, 
只计算mask中为True的部分, 
针对mask所对应的block中的每个值, 使用traversal算法, 修改field中的值
traversal算法: 首先找到polygon在该block中离左上方最近的顶点(注意优先判断离上方最近, 其次是离左侧最近),
然后从该点开始, 向右遍历, 直到出block边界或者该点不在polygon内, 
就往下一个单位, 判断是否在polygon内, 然后开始向左遍历, 直到出block边界或者该点不在polygon内, 就往下一个单位, 
在重复上述过程中, 遍历的方向会左右改变, 直到遍历到最后一行的出block边界或者该点不在polygon内
"""
def traverseMask(mask, block_size, field, x_min, x_max, y_min, y_max, polygon):
    # TODO: implement this function
    ...