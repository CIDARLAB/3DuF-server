import json
import sys

from parchmint import Device

sys.path.append("/usr/lib/freecad-python3/lib")
import Draft
import FreeCAD
import Mesh
import Part
from threedprinting.components.box import Box
from threedprinting.components.connection import createConnection
from threedprinting.components.droplet import DropletGenerator
from threedprinting.components.port import Port
from threedprinting.export import exportToSTL

myDocument = FreeCAD.newDocument()

UM_MM = 1000  # Constant to convert um to mm

file_path = sys.argv[1]
print("File Name: " + file_path)
device = None
with open(file_path) as data_file:
    text = data_file.read()
    device_json = json.loads(text)
    device = Device(device_json)

for component in device.components:
    if component.entity == "PORT":
        print("port")

        x = (component.xpos) / UM_MM
        y = (component.ypos) / UM_MM

        dictionary = component.__dict__
        params = dictionary["params"]
        height = params.get_param("height") / UM_MM
        pos = [x, y, -height / 2]
        radius = params.get_param("portRadius") / UM_MM
        port = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Port")
        Port(port, pos, radius=radius, height=height)
        myDocument.recompute()

    elif component.entity == "NOZZLE DROPLET GENERATOR":
        print("droplet")

        x = (component.xpos) / UM_MM
        y = (component.ypos) / UM_MM

        dictionary = component.__dict__
        params = dictionary["params"]
        waterInputWidth = params.get_param("waterInputWidth") / UM_MM
        oilInputWidth = params.get_param("oilInputWidth") / UM_MM
        orificeSize = params.get_param("orificeSize") / UM_MM
        orificeLength = params.get_param("orificeLength") / UM_MM
        outputLength = params.get_param("outputLength") / UM_MM
        outputWidth = params.get_param("outputWidth") / UM_MM
        height = params.get_param("height") / UM_MM
        pos = [x, y, -height / 2]

        droplet = FreeCAD.ActiveDocument.addObject(
            "Part::FeaturePython", "DropletGenerator"
        )
        DropletGenerator(
            droplet,
            pos,
            waterInputWidth,
            oilInputWidth,
            orificeSize,
            orificeLength,
            outputLength,
            outputWidth,
            height,
        )
        myDocument.recompute()

    else:
        print(component.entity, "not implemented")
        x = (component.xpos) / UM_MM
        y = (component.ypos) / UM_MM
        height = params.get_param("height") / UM_MM
        pos = [x, y, -height / 2]
        width = component.xspan / UM_MM
        length = component.yspan / UM_MM
        box = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Box")
        Box(box, pos, height=height, width=width, length=length)
        myDocument.recompute()

connections = []
for connection in device.connections:
    print(connection.name)
    dictionary = connection.__dict__
    waypoints = dictionary["params"].get_param("wayPoints")
    channelWidth = dictionary["params"].get_param("channelWidth")
    height = dictionary["params"].get_param("height")
    P = []
    for (x, y) in waypoints:
        x = x / UM_MM
        y = y / UM_MM
        P.append((x, y, 0))

    connectionObject = createConnection(
        P,
        myDocument,
        Type="CIRCLE",
        channelWidth=channelWidth / UM_MM,
        height=height / UM_MM,
    )
    connections.append(connectionObject)


objects = []
for obj in FreeCAD.ActiveDocument.Objects:
    print(obj.Name)
    objects.append(obj)

objects += connections
exportToSTL(objects, "DropletTest")
