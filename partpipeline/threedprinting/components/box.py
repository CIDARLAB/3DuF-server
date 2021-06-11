import sys

sys.path.append("/usr/lib/freecad-python3/lib")
sys.path.append("/home/ubuntu/3DuF-server/partpipeline/threedprinting")
import Draft
import FreeCAD
import Mesh
import Part
from export import exportToSTL


class Box:
    def __init__(self, obj, position=[0, 0, 0], width=10.0, height=10.0, length=10.0):
        """Add some custom properties to our port feature"""
        [x, y, z] = position
        pnt = FreeCAD.Vector(x, y, z)
        obj.addProperty(
            "App::PropertyLength", "Width", "Box", "Width of the box"
        ).Width = width
        obj.addProperty(
            "App::PropertyLength", "Height", "Box", "Height of the box"
        ).Height = height
        obj.addProperty(
            "App::PropertyLength", "Length", "Box", "Length of the box"
        ).Length = length
        obj.addProperty(
            "App::PropertyPosition", "Position", "Box", "Position of the box"
        ).Position = pnt
        obj.Proxy = self
        obj.Label = "3DuF_Object"

    def onChanged(self, fp, prop):
        """Do something when a property has changed"""
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

    def execute(self, fp):
        """Do something when doing a recomputation, this method is mandatory"""
        fp.Shape = Part.makeBox(fp.Width, fp.Length, fp.Height, fp.Position)


def makeBox(position, width=10.0, height=10.0, length=10.0):
    D = FreeCAD.newDocument()
    a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Box")

    Box(a, position=position, width=width, height=height, length=length)
    D.recompute()
    return a


# exportToSTL([makeBox([0,0,0])], u"Box")
