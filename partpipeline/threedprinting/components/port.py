import sys
sys.path.append("/usr/lib/freecad-python3/lib")
sys.path.append("/home/ubuntu/3DuF-server/partpipeline/threedprinting")
import FreeCAD, Draft, Part
import Mesh
from export import exportToSTL

class Port:
    def __init__(self, obj, position=[0,0,0], radius=0.005, height=0.010):
        '''Add some custom properties to our port feature'''
        [x,y,z] = position
        pnt = FreeCAD.Vector(x,y,z)
        direction = FreeCAD.Vector(0,0,1)
        obj.addProperty("App::PropertyLength","Radius","Port","Radius of the port").Radius=radius
        obj.addProperty("App::PropertyLength","Height","Port", "Height of the port").Height=height
        obj.addProperty("App::PropertyPosition", "Position", "Port", "Position of the port").Position=pnt
        obj.addProperty("App::PropertyDirection", "Direction", "Port", "Direction of the port").Direction=direction
        obj.Proxy = self
        obj.Label = "3DuF_Object"
   
    def onChanged(self, fp, prop):
        '''Do something when a property has changed'''
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")
 
    def execute(self, fp):
        '''Do something when doing a recomputation, this method is mandatory'''
        fp.Shape = Part.makeCylinder(fp.Radius, fp.Height, fp.Position, fp.Direction)

def makePort(position, radius=0.005, height=0.010):
    D=FreeCAD.newDocument()
    a=FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Port")
    Port(a, radius=radius, height=height)
    D.recompute()
    return a
