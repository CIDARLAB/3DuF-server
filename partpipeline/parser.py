from parchmint import Device
import sys
import json

sys.path.append("/usr/lib/freecad-python3/lib")
import FreeCAD, Draft, Part, Mesh

from threedprinting.components.port import Port
from threedprinting.components.droplet import DropletGenerator
from threedprinting.components.connection import createConnection
from threedprinting.components.box import Box
from threedprinting.export import exportToSTL

myDocument = FreeCAD.newDocument()

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

        x = (component.xpos)
        y = (component.ypos)

        dictionary = component.__dict__
        params = dictionary["params"]
        height = params.get_param("height")
        pos = [x,y,-height//2]
        radius = params.get_param("portRadius")
        port = FreeCAD.addObject("Part::FeaturePython", "Port")
        Port(port, pos, radius=radius, height=height)
        myDocument.recompute()
    elif component.entity == "NOZZLE DROPLET GENERATOR":
        print("droplet")

        x = (component.xpos)
        y = (component.ypos)

        dictionary = component.__dict__
        params = dictionary["params"]
        waterInputWidth = params.get_param("waterInputWidth")
        oilInputWidth = params.get_param("oilInputWidth")
        orificeSize = params.get_param("orificeSize")
        orificeLength = params.get_param("orificeLength")
        outputLength = params.get_param("outputLength")
        outputWidth = params.get_param("outputWidth")
        height = params.get_param("height")
        pos = [x,y,-height//2]

        print(waterInputWidth,oilInputWidth,orificeLength,orificeSize,outputLength,outputWidth)

        droplet = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "DropletGenerator")
        DropletGenerator(droplet, pos, waterInputWidth, oilInputWidth, orificeSize,orificeLength,outputLength,outputWidth)
        myDocument.recompute()
    else:
        print(component.entity, "not implemented")
        x = (component.xpos)
        y = (component.ypos)
        print(x,y)
        height = params.get_param("height")
        pos = [x,y,-height//2]
        width = component.xspan
        length = component.yspan
        box = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Box")
        Box(box, pos, height=height, width=width, length=length)
        myDocument.recompute()
for connection in device.connections:
    dictionary = connection.__dict__
    waypoints = dictionary["params"].get_param("wayPoints")
    P = []
    for (x,y) in waypoints:
        x = x
        y = y
        P.append((x,y,0))
    
    connectionObject = createConnection(P)
    connections.append(connectionObject)


objects = []
for obj in FreeCAD.ActiveDocument.Objects:
    objects.append(obj)

exportToSTL(objects, "parsed")

