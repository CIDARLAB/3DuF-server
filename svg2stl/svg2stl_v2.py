import FreeCAD
import re
import importSVG
import Part
from FreeCAD import Vector
import Mesh

SUBSTRATE_Z_DIM = 3000 / 1000

# my Objects - array of FreeCAD objects
def exportToSTL(myObjects, directory):
    __objs__ = []
    for myObject in myObjects:
        print(myObject)
        __objs__.append(myObject)
    Mesh.export(__objs__, directory + u".stl")


def extrudeSVGObject(object, doc, z_depth):
    SVG = object  # doc.Objects[i]
    if "Shape" not in dir(SVG):
        print("I'm not sure what this part is with the shape ?")

    if SVG.Shape.ShapeType not in ("Wire", "Edge"):
        print("Skipping shape {0} of type {1}".format(SVG.Name, SVG.Shape.ShapeType))

    try:
        tmp = Part.Face(Part.Wire(Part.__sortEdges__(SVG.Shape.Edges)))
        if tmp.isNull():
            raise ValueError("Face is null")

        SVGFace = doc.addObject("Part::Feature", "SVGFace")
        SVGFace.Shape = tmp
        del tmp

        # Extrude the face
        SVGExtrude = doc.addObject("Part::Extrusion", "SVGExtrudeOutline")
        SVGExtrude.Base = SVGFace
        SVGExtrude.Dir = Vector(0, 0, -z_depth)
        SVGExtrude.Solid = True
        SVGExtrude.TaperAngle = 0
        return SVGExtrude

    except ValueError:
        print("Skipping shape {0}".format(SVG.Name))

    except Part.OCCError:
        print("Skipping shape {0}".format(SVG.Name))


def extrudeSVGObjectPorts(objects, doc, z_depth):
    print("Port Objects:", objects)
    ret = []
    for object in objects:
        SVG = object  # doc.Objects[i]
        if "Shape" not in dir(SVG):
            print("I'm not sure what this part is with the shape ?")

        if SVG.Shape.ShapeType not in ("Wire", "Edge"):
            print(
                "Skipping shape {0} of type {1}".format(SVG.Name, SVG.Shape.ShapeType)
            )

        try:
            tmp = Part.Face(Part.Wire(Part.__sortEdges__(SVG.Shape.Edges)))
            if tmp.isNull():
                raise ValueError("Face is null")

            SVGFace = doc.addObject("Part::Feature", "SVGFace")
            SVGFace.Shape = tmp
            del tmp

            # Extrude the face
            SVGExtrude = doc.addObject("Part::Extrusion", "SVGEPortsExtrude")
            SVGExtrude.Base = SVGFace
            SVGExtrude.Dir = Vector(0, 0, -z_depth)
            SVGExtrude.Solid = True
            SVGExtrude.TaperAngle = 0
            ret.append(SVGExtrude)

        except ValueError:
            print("Skipping shape {0}".format(SVG.Name))

        except Part.OCCError:
            print("Skipping shape {0}".format(SVG.Name))


# file_name = "flow_0_250.svg"
file_name = "COMPONENT_FLOW_0_312.svg"

outline_filename = "UniversalEdge.svg"

ports_filename = "PORT_FLOW_0_1100.svg"

# Read the file and break apart the name based on regex
pattern = r"([A-Z]+)_([A-Z]+)_(\d+)_(\d+).svg"

# Save first group variable as modifier
modifier = re.search(pattern, file_name).group(1)

# Save second group variable as layer type
layer_type = re.search(pattern, file_name).group(2)

# Save third group variable as layer number
substrate_number = re.search(pattern, file_name).group(3)

# Save the fourth group variable as the feature layer depth
z_depth = SUBSTRATE_Z_DIM

# Save fourth group variable as z depth
z_depth = float(re.search(pattern, file_name).group(4)) / 1000

print(modifier, layer_type, substrate_number, z_depth)

doc = FreeCAD.newDocument(file_name.replace(".svg", ""))

# Import the SVG file
importSVG.insert(filename=file_name, docname=doc.Name)

# Get the number of objects in the document
num_objects = len(doc.Objects)

extrude_objects = []

# # Get the imported object
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
    SVGExtrude.Dir = Vector(0, 0, -z_depth)
    SVGExtrude.Solid = True
    SVGExtrude.TaperAngle = 0
    SVGExtrude.Symmetric = False

    print("Created Extrude: " + SVGExtrude.Name)
    extrude_objects.append(SVGExtrude)
    # SVGFace.ViewObject.Visibility = False

doc.recompute()

# doc.saveCopy(file_name.replace(".svg", ".FCStd"))
new_count = len(doc.Objects)
# Generate the negative out of the positive substrate
importSVG.insert(filename=ports_filename, docname=doc.Name)

outline_extrude_object = extrudeSVGObjectPorts(
    doc.Objects[new_count::], doc, SUBSTRATE_Z_DIM
)

doc.recompute()


exportToSTL(doc.Objects[num_objects::], "design_with_ports")

# Generate the negative out of the positive substrate
importSVG.insert(filename=outline_filename, docname=doc.Name)

outline_extrude_object = extrudeSVGObject(doc.Objects[-1], doc, SUBSTRATE_Z_DIM)

doc.recompute()

exportToSTL(doc.Objects[num_objects::], file_name.replace(".svg", "") + "_outline")

# Run through all the different extrude objects and subtract them from the outline extrude object
for extrude_object in extrude_objects:
    doc.addObject("Part::Cut", "Cut")
    doc.Cut.Base = doc.getObject("SVGExtrudeOutline")
    doc.Cut.Tool = doc.getObject(extrude_object.Name)
    doc.recompute()
    # outline_extrude_object.Shape.cut(extrude_object)

doc.saveCopy(file_name.replace(".svg", ".FCStd"))

exportToSTL(doc.Objects[num_objects::], file_name.replace(".svg", "") + "_negative")

print(len(doc.Objects))
# Delete objects
# for extrude_object in extrude_objects:
#     doc.removeObject(extrude_object.Name)
#     doc.recompute()

print(len(doc.Objects))
exportToSTL([], file_name.replace(".svg", "") + "_negative_deleted")
