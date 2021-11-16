import re
from typing import List

import BOPTools.JoinFeatures
import importSVG
import Mesh
import Part
from FreeCAD import Vector

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


def reduce_join(join_objects, doc, iter_level=1):
    print("Starting reduce_join : " + str(iter_level))
    join_objects_copy = join_objects.copy()
    new_joined_objects = []
    skip_list = []
    intersection_found_flag = False
    # Try joining the objects
    for i in range(len(join_objects_copy)):
        for j in range(i + 1, len(join_objects_copy)):
            if {join_objects_copy[i], join_objects_copy[j]} in skip_list:
                continue
            elif i == j:
                continue

            f1 = doc.getObject(join_objects_copy[i])
            f2 = doc.getObject(join_objects_copy[j])

            # Find the intersection of the two faces
            intersection = f1.Shape.common(f2.Shape)
            # If the intersection is greater than zero then we can join the faces
            if intersection.Area > 0:
                intersection_found_flag = True
                j = doc.addObject("Part::Feature", "joinface_" + str(iter_level))
                j.Shape = f1.Shape.fuse(f2.Shape)

                print(
                    "Joining: {} , {} + {}, Intersection area: {}".format(
                        j.Name, f1.Name, f2.Name, intersection.Area
                    )
                )

                new_joined_objects.append(j.Name)
                skip_list.append({f1.Name, f2.Name})
                # # Remove the faces from the list
                # doc.removeObject(f1.Name)
                # doc.removeObject(f2.Name)

    # Call the next iteration recursively if any intersection was found
    if intersection_found_flag:
        iter_level += 1
        # Remove all the skip list items in the join_objects list
        for item in skip_list:
            join_objects.remove(item)
        # Add the new joined objects to the join_objects list
        join_objects.extend(new_joined_objects)
        print("New join objects:", join_objects)
        reduce_join(join_objects, doc, iter_level)
    else:
        print("No intersection found in iter: " + str(iter_level))
        print("Exiting Iterative join")


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

face_objects = []

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
        face_objects.append(SVGFace.Name)
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
    # SVGFace.ViewObject.Visibility = False

doc.recompute()

doc.saveCopy("shape_test" + ".FCStd")

# Now try joining each and every object together
joined_objects = []
skip_list = []
for i in range(len(face_objects)):
    for j in range(i, len(face_objects)):
        # If both are the same, skip
        # Check and see if the two shapes have any intersection / are joinabel
        # the face objec references
        if i == j:
            continue
        elif {face_objects[i], face_objects[j]} in skip_list:
            continue

        f1 = doc.getObject(face_objects[i])
        f2 = doc.getObject(face_objects[j])
        # Find the intersection of the two faces
        intersection = f1.Shape.common(f2.Shape)
        # If the intersection is not null, then we can join them together
        if intersection.Area > 0:
            j = doc.addObject("Part::Feature", "joinface")
            shp = f1.Shape.fuse(f2.Shape)
            j.Shape = shp
            # j = BOPTools.JoinFeatures.makeConnect(name="Connect")
            print(
                "Joining: {} , {} + {}, Intersection area: {}".format(
                    j.Name, f1.Name, f2.Name, intersection.Area
                )
            )
            # j.Objects = [f1, f2]
            # j.Proxy.execute(j)
            # j.purgeTouched()
            joined_objects.append(j.Name)
            skip_list.append({f1.Name, f2.Name})

            # # for obj in j.ViewObject.Proxy.claimChildren():
            # #     obj.ViewObject.hide()

# Remove all the original faces from the document
delete_list = []
for skip_set in skip_list:
    for name in list(skip_set):
        delete_list.append(name)

for name in set(delete_list):
    doc.removeObject(name)

doc.recompute()
doc.saveCopy("join_test_initial_step" + ".FCStd")

print("Initial join objects:", joined_objects)

# Iteratively join all the objects together
reduce_join(joined_objects, doc)
print(joined_objects)

doc.recompute()
doc.saveCopy("join_test_final_step" + ".FCStd")

# Now that all the joins are done, refine the shape by removing splinters
for i in range(len(joined_objects)):
    feature = doc.getObject(joined_objects[i])
    refined_shape = doc.addObject("Part::Feature", "RefinedShape")
    refined_shape.Shape = feature.Shape.removeSplitter()

doc.recompute()
doc.saveCopy("join_test_refined" + ".FCStd")

exit(0)


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
