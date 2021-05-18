import sys

sys.path.append("/usr/lib/freecad-python3/lib")
import FreeCAD, Draft, Part
import Mesh

# my Objects - array of FreeCAD objects
def exportToSTL(myObjects,directory):
    __objs__ = []
    for myObject in myObjects:
        __objs__.append(myObject)
    Mesh.export(myObjects,directory + u".stl")
    return None