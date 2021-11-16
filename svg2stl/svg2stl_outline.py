import re

import Draft
import FreeCAD
import importSVG
import Mesh
import Part
import SketcherObject
from FreeCAD import Vector


# my Objects - array of FreeCAD objects
def exportToSTL(myObjects, directory):
    __objs__ = []
    for myObject in myObjects:
        print(myObject)
        __objs__.append(myObject)
    Mesh.export(__objs__, directory + u".stl")


file_name = "flow_0_250.svg"

# Read the file and break apart the name based on regex
pattern = r"((\w+)_)?(\w+)_(\d+)_(\d+).svg"

# Save first group variable as modifier
modifier = re.search(pattern, file_name).group(2)

# Save second group variable as layer type
layer_type = re.search(pattern, file_name).group(3)

# Save third group variable as layer number
layer_number = re.search(pattern, file_name).group(4)

# Save fourth group variable as z depth
z_depth = float(re.search(pattern, file_name).group(5)) / 1000

print(modifier, layer_type, layer_number, z_depth)

doc = FreeCAD.newDocument("flow")

print("Number of objects in the document: " + str(len(doc.Objects)))


# Import the SVG file
importSVG.insert(filename=file_name, docname=doc.Name)

# Get the number of objects in the document
num_objects = len(doc.Objects)

print("Number of objects in the document: " + str(num_objects))
print(doc.Objects)
sketch = doc.addObject("Sketcher::SketchObject", "CombinedSketch")
print(doc.Objects)


# turn the inported objects into sketches
i = 0
for obj in doc.Objects:
    print(type(obj))
    print(i)
    i += 1
    if isinstance(obj, SketcherObject):
        print("Sketch")
        continue
    Draft.makeSketch(obj, autoconstraints=False, addTo=sketch)
    doc.removeObject(obj.Name)

# merge the sketches into a single sketch
# can be done in gui, but does not appear to be accessible via python
# so we try to do it manually by adding the geometries and constraints
# (not that there will be any constraints, but if later we re-use this code...)
# for obj in doc.Objects:
#     if obj.Label == sketch.Name:
#         continue
#     if hasattr(obj,'Geometry'):
#         for geo in obj.Geometry:
#             sketch.addGeometry(geo)
#     if hasattr(obj,'Constraints'):
#         for con in obj.Constraints:
#             sketch.addConstraint(con)
#     doc.removeObject(obj.Label)


print(doc.Objects)


# # Get the imported object
# for i in range(len(doc.Objects)):
#     SVG = doc.Objects[i]
#     if 'Shape' not in dir(SVG):
#         print("I'm not sure what this part is with the shape ?")
#         continue
#     if SVG.Shape.ShapeType not in ('Wire', 'Edge'):
#             print("Skipping shape {0} of type {1}".format(SVG.Name, SVG.Shape.ShapeType))
#             continue

#     try:
#         tmp = Part.Face(Part.Wire(Part.__sortEdges__(SVG.Shape.Edges)))
#         if tmp.isNull():
#             raise ValueError("Face is null")

#         SVGFace = doc.addObject("Part::Feature", "SVGFace")
#         SVGFace.Shape = tmp
#         del tmp
#     except ValueError:
#         print("Skipping shape {0}".format(SVG.Name))
#         continue
#     finally:
#         # SVG.ViewObject.Visibility = False
#         pass

#     # Extrude the face
#     SVGExtrude = doc.addObject("Part::Extrusion", "SVGExtrude")
#     SVGExtrude.Base = SVGFace
#     SVGExtrude.Dir = Vector(0, 0, z_depth)
#     SVGExtrude.Solid = True
#     SVGExtrude.TaperAngle = (0)
#     # SVGFace.ViewObject.Visibility = False

doc.recompute()

exportToSTL(doc.Objects[num_objects::], "test_outline")
