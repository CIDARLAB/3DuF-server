import sys

sys.path.append("/usr/lib/freecad-python3/lib")
import Draft
import FreeCAD
import Mesh
import Part


class Component:
    def __init__(self, obj, entity, position, params):
        """Add some custom properties to our General Component feature"""
        [x, y, z] = position
        pnt = FreeCAD.Vector(x, y, z)

        for key, item in params.items():
            print(key, item)
            setattr(
                obj.addProperty(
                    "App::PropertyLength", key, entity, key + "of component"
                ),
                key,
                item,
            )

        obj.addProperty(
            "App::PropertyPosition", "Position", entity, "Position of component"
        ).Position = pnt
        obj.addProperty(
            "App::PropertyString", "Type", entity, "Type of component"
        ).__entity = entity

        obj.Proxy = self
        obj.Label = "3DuF_Object"

    @staticmethod
    def execute(fp):
        myDocument = FreeCAD.open(
            u"/home/ubuntu/3DuF-server/partpipeline/threedprinting/components/sources/"
            + fp.__entity
            + u".FCStd"
        )
