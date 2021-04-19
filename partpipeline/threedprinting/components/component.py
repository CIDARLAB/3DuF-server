class Component:
    def __init__(self, obj, position, params):
        [x,y,z] = position
        pnt = FreeCAD.Vector(x,y,z)

        for key, item in params.items():
            print(key, item)
        obj.Proxy = self
    
    def execute():
        