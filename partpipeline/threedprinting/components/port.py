import sys
sys.path.append("/usr/lib/freecad-python3/lib")
import FreeCAD, Draft, Part
import Mesh

def createPort(position, radius=5, height = 10):
    D = FreeCAD.newDocument()
    
    [x,y,z] = position
    pnt = FreeCAD.Vector(x,y,z)

    direction = FreeCAD.Vector(0,0,1)

    cylinder = Part.makeCylinder(radius, height, pnt, direction)

    obj = D.addObject("Part::Feature", "Section")
    obj.Shape = cylinder

    D.recompute()
    return obj


# pos = [0,0,0]
# exportToSTL([createPort(pos)],u"Test")