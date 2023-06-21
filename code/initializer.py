import numpy as np


def initPolygonList_custom(vertexesList):
    """
    初始化一个多边形列表, 每个多边形由vertexesList中的顶点组成
    """
    polygonList = []
    for vertexes in vertexesList:
        polygonList.append(initPolygonFromVertexes(vertexes))
    return polygonList


def initPolygonList_random(nPolygons, nVertexes, x_max, y_max):
    """
    随机初始化一个多边形列表, 每个多边形由nVertexes个顶点组成
    """
    polygonList = []
    for i in range(nPolygons):
        polygonList.append(initRandomPolygon(nVertexes, x_max, y_max))
    return polygonList


def initPolygonFromVertexes(vertexes):
    """
    初始化一个多边形, 由vertexes中的顶点组成
    注意计算质心来保证生成的多边形是逆时针的
    """
    # calculate centroid
    centroid = np.mean(vertexes, axis=0)

    # sort vertexes by angle
    vertexes = sorted(vertexes, key=lambda v: np.arctan2(v[1] - centroid[1], v[0] - centroid[0]))

    # if you want to ensure clockwise order, just reverse the list
    # vertexes = list(reversed(vertexes))

    polygon = np.array(vertexes)
    return polygon


def initRandomPolygon(nVertexes, x_max, y_max):
    """
    初始化一个随机多边形, 由nVertexes个顶点组成
    """
    vertexes = []
    for i in range(nVertexes):
        vertexes.append([np.random.uniform(0, x_max), np.random.uniform(0, y_max)])
    return initPolygonFromVertexes(vertexes)
