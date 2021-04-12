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

        x = (component.xpos)/1000
        y = (component.ypos)/1000

        dictionary = component.__dict__
        params = dictionary["params"]
        height = params.get_param("height")/1000
        pos = [x,y,-height/2]
        radius = params.get_param("portRadius")/1000
        port = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Port")
        Port(port, pos, radius=radius, height=height)
        myDocument.recompute()
    elif component.entity == "NOZZLE DROPLET GENERATOR":
        print("droplet")

        x = (component.xpos)/1000
        y = (component.ypos)/1000

        dictionary = component.__dict__
        params = dictionary["params"]
        waterInputWidth = params.get_param("waterInputWidth")/1000
        oilInputWidth = params.get_param("oilInputWidth")/1000
        orificeSize = params.get_param("orificeSize")/1000
        orificeLength = params.get_param("orificeLength")/1000
        outputLength = params.get_param("outputLength")/1000
        outputWidth = params.get_param("outputWidth")/1000
        height = params.get_param("height")/1000
        pos = [x,y,-height/2]

        print(waterInputWidth,oilInputWidth,orificeLength,orificeSize,outputLength,outputWidth, height)

        droplet = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "DropletGenerator")
        DropletGenerator(droplet, pos, waterInputWidth, oilInputWidth, orificeSize, orificeLength, outputLength, outputWidth, height)
        myDocument.recompute()
    else:
        print(component.entity, "not implemented")
        x = (component.xpos)/1000
        y = (component.ypos)/1000
        print(x,y)
        height = params.get_param("height")/1000
        pos = [x,y,-height/2]
        width = component.xspan/1000
        length = component.yspan/1000
        box = FreeCAD.ActiveDocument.addObject("Part::FeaturePython", "Box")
        Box(box, pos, height=height, width=width, length=length)
        myDocument.recompute()

connections = []
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

objects += connections

exportToSTL(objects, "DropletGenerator")

