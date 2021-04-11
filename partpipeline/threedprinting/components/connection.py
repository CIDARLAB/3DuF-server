import sys

sys.path.append("/usr/lib/freecad-python3/lib")
import FreeCAD, Draft, Part
import Mesh

# class Connection:
#     def __init__(self, obj, waypoints, type="circular"):

# waypoints - Array of waypoints in form (x,y,z) tuple
def createConnection(waypoints, radius=3):
    D = FreeCAD.newDocument()

    # Path in XYZ
    P = waypoints  # needs to be at least of length 2

    if len(waypoints) < 2:
        raise ValueError 

    # Circle to make the cross section of Connection
    pnt = FreeCAD.Vector(P[0][0],P[0][1],P[0][2])
    # 
    print(pnt)
    [x,y,z] = [P[1][0] - P[0][0], P[1][1] - P[0][1], P[1][2] - P[0][2]]

    direction = FreeCAD.Vector(x,y,z)  # which initial direction
    print(direction)
    circle = Part.makeCircle(radius,pnt,direction)

    # Circle Object
    obj = D.addObject("Part::Feature", "Section")
    obj.Shape = circle
    w=Draft.makeWire(P)

    # Sweep object/Connection
    sw = D.addObject('Part::Sweep','Sweep')
    sw.Sections=[D.Section, ]
    edges = ["Edge"+str(x+1) for x in range(len(P)-1)]
    print(edges)
    sw.Spine=(w,edges)  # Depends on number of waypoints
    sw.Solid=True
    sw.Frenet=False
    D.recompute()
    return sw  # FreeCAD object of connection


# P=[]
# P.append((0,0,0))  # waypoints
# P.append((100,0,0))
# P.append((120,50,0))
# P.append((120,70,40))
# exportToSTL([createConnection(P)],u"Test2")