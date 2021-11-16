import re

import FreeCAD
import importSVG
import Mesh
import Part
from FreeCAD import Vector

SUBSTRATE_Z_DIM = 3000

# my Objects - array of FreeCAD objects
def exportToSTL(myObjects, directory):
    __objs__ = []
    for myObject in myObjects:
        print(myObject)
        __objs__.append(myObject)
    Mesh.export(__objs__, directory + u".stl")


# file_name = "flow_0_250.svg"
file_name = "EDGE_flow_0.svg"

# Read the file and break apart the name based on regex
pattern = r"((\w+)_)?(\w+)_(\d+)(_(\d+))?.svg"

# Save first group variable as modifier
modifier = re.search(pattern, file_name).group(2)

# Save second group variable as layer type
layer_type = re.search(pattern, file_name).group(3)

# Save third group variable as layer number
substrate_number = re.search(pattern, file_name).group(4)

z_depth = SUBSTRATE_Z_DIM
# Save fourth group variable as z depth
if re.search(pattern, file_name).group(6) != None:
    z_depth = float(re.search(pattern, file_name).group(6)) / 1000

print(modifier, layer_type, substrate_number, z_depth)

doc = FreeCAD.newDocument("flow")

# Import the SVG file
importSVG.insert(filename=file_name, docname=doc.Name)

# Get the number of objects in the document
num_objects = len(doc.Objects)

# Get the imported object
for i in range(len(doc.Objects)):
    SVG = doc.Objects[i]
    if "Shape" not in dir(SVG):
        print("I'm not sure what this part is with the shape ?")
        continue
    if SVG.Shape.ShapeType not in ("Wire", "Edge"):
        print("Skipping shape {0} of type {1}".format(SVG.Name, SVG.Shape.ShapeType))
        continue

    try:
        tmp = Part.Face(Part.Wire(Part.__sortEdges__(SVG.Shape.Edges)))
        if tmp.isNull():
            raise ValueError("Face is null")

        SVGFace = doc.addObject("Part::Feature", "SVGFace")
        SVGFace.Shape = tmp
        del tmp
    except ValueError:
        print("Skipping shape {0}".format(SVG.Name))
        continue
    except Part.OCCError:
        print("Skipping shape {0}".format(SVG.Name))
        continue
    finally:
        # SVG.ViewObject.Visibility = False
        pass

    # Extrude the face
    SVGExtrude = doc.addObject("Part::Extrusion", "SVGExtrude")
    SVGExtrude.Base = SVGFace
    SVGExtrude.Dir = Vector(0, 0, z_depth)
    SVGExtrude.Solid = True
    SVGExtrude.TaperAngle = 0
    # SVGFace.ViewObject.Visibility = False

doc.recompute()

exportToSTL(doc.Objects[num_objects::], "test")
