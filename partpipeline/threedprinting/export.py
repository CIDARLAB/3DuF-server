import sys

sys.path.append("/usr/lib/freecad-python3/lib")
import Draft
import FreeCAD
import Mesh
import Part


# my Objects - array of FreeCAD objects
def exportToSTL(myObjects, directory):
    __objs__ = []
    for myObject in myObjects:
        print(myObject)
        __objs__.append(myObject)
    Mesh.export(__objs__, directory + u".stl")
    return None
