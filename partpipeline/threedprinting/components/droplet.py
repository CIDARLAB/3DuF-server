import sys

sys.path.append("/usr/lib/freecad-python3/lib")
import Draft
import FreeCAD
import Mesh
import Part

sys.path.append("/home/ubuntu/3DuF-server/partpipeline/threedprinting")

from export import exportToSTL


class DropletGenerator:
    def __init__(
        self,
        obj,
        position=[0, 0, 0],
        waterInputWidth=0.6,
        oilInputWidth=0.6,
        orificeSize=0.2,
        orificeLength=0.4,
        outputLength=0.6,
        outputWidth=0.6,
        height=0.25,
    ):
        """Add some custom properties to our Droplet Generator feature"""
        [x, y, z] = position
        pnt = FreeCAD.Vector(x, y, z)

        obj.addProperty(
            "App::PropertyPosition",
            "Position",
            "DropletGenerator",
            "Position of the Droplet Generator",
        ).Position = pnt
        obj.addProperty(
            "App::PropertyLength",
            "waterInputWidth",
            "DropletGenerator",
            "Water Input Width of the Droplet Generator",
        ).waterInputWidth = waterInputWidth
        obj.addProperty(
            "App::PropertyLength",
            "oilInputWidth",
            "DropletGenerator",
            "Oil Input Width of the Droplet Generator",
        ).oilInputWidth = oilInputWidth
        obj.addProperty(
            "App::PropertyLength",
            "orificeSize",
            "DropletGenerator",
            "Orifice Size of the Droplet Generator",
        ).orificeSize = orificeSize
        obj.addProperty(
            "App::PropertyLength",
            "orificeLength",
            "DropletGenerator",
            "Orifice Length of the Droplet Generator",
        ).orificeLength = orificeLength
        obj.addProperty(
            "App::PropertyLength",
            "outputLength",
            "DropletGenerator",
            "Output Length of the Droplet Generator",
        ).outputLength = outputLength
        obj.addProperty(
            "App::PropertyLength",
            "outputWidth",
            "DropletGenerator",
            "Output Width of the Droplet Generator",
        ).outputWidth = outputWidth
        obj.addProperty(
            "App::PropertyLength",
            "height",
            "DropletGenerator",
            "Height of the Droplet Generator",
        ).height = height
        obj.Proxy = self
        obj.Label = "3DuF_Object"

    def onChanged(self, fp, prop):
        """Do something when a property has changed"""
        FreeCAD.Console.PrintMessage("Change property: " + str(prop) + "\n")

    def execute(self, fp):
        """Do something when doing a recomputation, this method is mandatory"""
        myDocument = FreeCAD.open(
            u"/home/ubuntu/3DuF-server/partpipeline/threedprinting/components/sources/DROPLET GENERATOR.FCStd"
        )

        sheet = myDocument.getObject("Spreadsheet")
        sketch = myDocument.getObject("Sketch")

        print("here1")
        sheet.set("waterInputWidth", str(fp.waterInputWidth))
        sheet.set("oilInputWidth", str(fp.oilInputWidth))
        sheet.set("orificeSize", str(fp.orificeSize))
        sheet.set("orificeLength", str(fp.orificeLength))
        sheet.set("outputLength", str(fp.outputLength))
        sheet.set("outputWidth", str(fp.outputWidth))
        sheet.set("height", str(fp.height))
        sheet.recompute()
        FreeCAD.ActiveDocument.recompute()
        print("here2")
        # sketch.setDatum("waterInputWidth",fp.waterInputWidth)
        # sketch.setDatum("oilInputWidth",fp.oilInputWidth)
        # sketch.setDatum("orificeSize",fp.orificeSize)
        # sketch.setDatum("orificeLength",fp.orificeLength)
        # sketch.setDatum("outputLength",fp.outputLength)
        # sketch.setDatum("outputWidth",fp.outputWidth)

        # wire = sketch.Shape.Wires[0]  # check
        extr = myDocument.Extrude
        # extr.setExpression('Dir.z',fp.height)
        # print(fp.height)

        # face = Part.Face(wire)
        # extr = face.extrude(FreeCAD.Vector(0,0,fp.height))

        fp.Shape = extr


def makeDroplet(
    position,
    waterInputWidth=0.600,
    oilInputWidth=0.600,
    orificeSize=0.200,
    orificeLength=0.300,
    outputLength=0.600,
    outputWidth=0.600,
    height=0.250,
):
    D = FreeCAD.newDocument()
    a = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "DropletGenerator")
    DropletGenerator(
        a,
        position,
        waterInputWidth,
        oilInputWidth,
        orificeSize,
        orificeLength,
        outputLength,
        outputWidth,
        height,
    )
    D.recompute()
    return a


# exportToSTL([makeDroplet([0,0,0])], u"DropletGenerator")
