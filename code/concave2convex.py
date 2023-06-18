from shapely.geometry import Polygon
import pyclipper

# 将凹多边形转化为凸多边形
def concave2convex(polygonList):
    convexPolygons = []
    for polygon in polygonList:
        if not isConvex(polygon):
            convexPolygons.append(getConvexHull(polygon))
        else:
            convexPolygons.append(polygon)
    return convexPolygons

# 判断多边形是否为凸多边形
def isConvex(polygon):
    polygon_shapely = Polygon(polygon)
    return polygon_shapely.is_valid and polygon_shapely.is_convex

# 计算凸包
def getConvexHull(polygon):
    pc = pyclipper.Pyclipper()
    pc.AddPath(pyclipper.scale_to_clipper(polygon), pyclipper.PT_SUBJECT, True)
    solution = pc.Execute(pyclipper.CT_UNION, pyclipper.PFT_EVENODD, pyclipper.PFT_EVENODD)
    convex_hull = [tuple(point) for point in pyclipper.scale_from_clipper(solution[0])]
    return convex_hull
