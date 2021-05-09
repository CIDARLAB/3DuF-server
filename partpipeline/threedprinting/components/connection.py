import sys

sys.path.append("/usr/lib/freecad-python3/lib")
import FreeCAD, Draft, Part
import Mesh

sys.path.append("/home/ubuntu/3DuF-server/partpipeline/threedprinting")
from export import exportToSTL

# class Connection:
#     def __init__(self, obj, waypoints, channelWidth, height, Type="circular"):
#         '''Add some custom properties to our Connection Feature'''
#         obj.addProperty("App::PropertyVectorList","Waypoints","Connection","Waypoints of Connection").waypoints=waypoints
#         obj.addProperty("App::PropertyType","Type","Connection","Cross Section Shape of Connection").type=Type
#         obj.addProperty("App::PropertyLength","ChannelWidth","Width of Connection").channelWidth = channelWidth
#         obj.addProperty("App::PropertyLength","height","Height of Connection").height = height
    
#     def execute(self, fp):
#         D = FreeCAD.ActiveDocument
#         P = fp.waypoints
#         if len(P) < 2:
#             return ValueError
#         pnt = FreeCAD.Vector(P[0][0],P[0][1],P[0][2])
#         # 
#         [x,y,z] = [P[1][0] - P[0][0], P[1][1] - P[0][1], P[1][2] - P[0][2]]

#         direction = FreeCAD.Vector(x,y,z)  # which initial direction
        
#         shape = None
#         if fp.type == "CIRCLE":
#             shape = Part.makeCircle(fp.channelWidth/2,pnt,direction)
#         elif fp.type == "RECTANGLE":
#             shape = Part.makePlane(fp.channelWidth,fp.height,pnt,direction)
#         else:
#             raise ValueError

#         # Circle Object
#         obj = D.addObject("Part::Feature", "Section")
#         obj.Shape = shape
#         w=Draft.makeWire(P)

#         # Sweep object/Connection
#         sw = D.addObject('Part::Sweep','Sweep')
#         sw.Sections=[D.Section, ]
#         edges = ["Edge"+str(x+1) for x in range(len(P)-1)]
#         sw.Spine=(w,edges)  # Depends on number of waypoints
#         sw.Solid=True
#         sw.Frenet=False
#         D.recompute()

#         fp.Shape = sw

# waypoints - Array of waypoints in form (x,y,z) tuple
def createConnection(waypoints, ActiveDocument, Type="CIRCLE",channelWidth=0.1, height=0.05):
    D = ActiveDocument

    # Path in XYZ
    P = waypoints  # needs to be at least of length 2

    if len(waypoints) < 2:
        raise ValueError 

    # 
    [x,y,z] = [P[1][0] - P[0][0], P[1][1] - P[0][1], P[1][2] - P[0][2]]

    direction = FreeCAD.Vector(x,y,z)  # which initial direction

    shape = None
    if Type == "CIRCLE":
        pnt = FreeCAD.Vector(P[0][0],P[0][1],P[0][2])
        shape = Part.makeCircle(channelWidth/2,pnt,direction)
    elif Type == "RECTANGLE":
        pnt = FreeCAD.Vector(P[0][0]-(channelWidth/2),P[0][1] - (height/2),P[0][2])
        shape = Part.makePlane(channelWidth,height,pnt,direction)
    else:
        raise ValueError

    # Circle Object
    obj = D.addObject("Part::Feature", "Section")
    obj.Shape = shape
    w=Draft.makeWire(P)
    print(P)

    # Sweep object/Connection
    sw = D.addObject('Part::Sweep','Sweep')
    sw.Sections=[D.Section, ]
    edges = ["Edge" + str(x+1) for x in range(len(P)-1)]
    print(edges, w)
    sw.Spine=(w,edges)  # Depends on number of waypoints
    sw.Solid=True
    sw.Frenet=False
    D.recompute()
    return sw  # FreeCAD object of connection


D = FreeCAD.newDocument()
P=[]
P.append((0,0,0))  # waypoints
P.append((10,0,0))
exportToSTL([createConnection(P,D, Type="RECTANGLE")],u"Test2")