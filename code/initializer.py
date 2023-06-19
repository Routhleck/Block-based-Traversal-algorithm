import numpy as np


def initPolygonList_custom(vertexesList):
    """
    Initialize a polygon list from a list of vertexes list.
    """
    polygonList = []
    for vertexes in vertexesList:
        polygonList.append(initPolygonFromVertexes(vertexes))
    return polygonList


def initPolygonList_random(nPolygons, nVertexes, x_max, y_max):
    """
    Initialize a random polygon list with nPolygons polygons, each polygon has nVertexes vertexes.
    """
    polygonList = []
    for i in range(nPolygons):
        polygonList.append(initRandomPolygon(nVertexes, x_max, y_max))
    return polygonList


def initPolygonFromVertexes(vertexes):
    """
    Initialize a polygon from a list of vertexes.
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
    Initialize a random polygon with nVertexes vertexes.
    """
    vertexes = []
    for i in range(nVertexes):
        vertexes.append([np.random.uniform(0, x_max), np.random.uniform(0, y_max)])
    return initPolygonFromVertexes(vertexes)
