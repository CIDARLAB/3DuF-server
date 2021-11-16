# Join Features

Use this to potentially fuse all the svg outputs

```
import BOPTools.JoinFeatures
j = BOPTools.JoinFeatures.makeConnect(name = 'Connect')
j.Objects = [App.ActiveDocument.Circle]
j.Proxy.execute(j)
j.purgeTouched()
for obj in j.ViewObject.Proxy.claimChildren():
    obj.ViewObject.hide()
j = BOPTools.JoinFeatures.makeConnect(name = 'Connect')
j.Objects = [App.ActiveDocument.Rectangle, App.ActiveDocument.Circle]
j.Proxy.execute(j)
j.purgeTouched()
for obj in j.ViewObject.Proxy.claimChildren():
    obj.ViewObject.hide()
```

```
>>> j = BOPTools.JoinFeatures.makeConnect(name = 'Connect')
>>> j.Objects = [App.ActiveDocument.Connect006, App.ActiveDocument.Connect, App.ActiveDocument.Connect005, App.ActiveDocument.Connect003, App.ActiveDocument.Connect004, App.ActiveDocument.Connect001]
>>> j.Proxy.execute(j)
>>> j.purgeTouched()
>>> for obj in j.ViewObject.Proxy.claimChildren():
>>>     obj.ViewObject.hide()
```


# Refine shape

removed all the edges, basically the `removeSplitter()` function was used

```
App.ActiveDocument.addObject('Part::Feature','Connect007').Shape=App.ActiveDocument.Connect007.Shape.removeSplitter()
App.ActiveDocument.ActiveObject.Label=App.ActiveDocument.Connect007.Label
Gui.ActiveDocument.Connect007.hide()
Gui.ActiveDocument.ActiveObject.ShapeColor=Gui.ActiveDocument.Connect007.ShapeColor
Gui.ActiveDocument.ActiveObject.LineColor=Gui.ActiveDocument.Connect007.LineColor
Gui.ActiveDocument.ActiveObject.PointColor=Gui.ActiveDocument.Connect007.PointColor
App.ActiveDocument.recompute()
```

# Full Log

```
Python 3.6.7 | packaged by conda-forge | (default, Nov 20 2018, 18:20:05) 
[GCC 4.2.1 Compatible Apple LLVM 9.0.0 (clang-900.0.37)] on darwin
Type 'help', 'copyright', 'credits' or 'license' for more information.
>>> MRU="0"
>>> exec(open('/Applications/FreeCAD.app/Contents/Resources/data/Mod/Start/StartPage/LoadMRU.py').read())
>>> App.setActiveDocument("shape_test")
>>> App.ActiveDocument=App.getDocument("shape_test")
>>> Gui.ActiveDocument=Gui.getDocument("shape_test")
>>> Gui.getDocument("shape_test").getObject("SVGFace").Visibility=True
>>> Gui.getDocument("shape_test").getObject("SVGFace001").Visibility=True
>>> Gui.getDocument("shape_test").getObject("SVGFace002").Visibility=True
>>> Gui.getDocument("shape_test").getObject("SVGFace003").Visibility=True
>>> Gui.getDocument("shape_test").getObject("SVGFace004").Visibility=True
>>> Gui.getDocument("shape_test").getObject("SVGFace005").Visibility=True
>>> Gui.getDocument("shape_test").getObject("SVGFace006").Visibility=True
>>> Gui.getDocument("shape_test").getObject("SVGFace007").Visibility=True
>>> Gui.getDocument("shape_test").getObject("SVGFace008").Visibility=True
>>> Gui.getDocument("shape_test").getObject("SVGFace009").Visibility=True
>>> Gui.getDocument("shape_test").getObject("SVGFace010").Visibility=True
>>> Gui.getDocument("shape_test").getObject("SVGFace011").Visibility=True
>>> Gui.getDocument("shape_test").getObject("SVGFace012").Visibility=True
>>> Gui.SendMsgToActiveView("ViewFit")
>>> Gui.activateWorkbench("PartWorkbench")
>>> import BOPTools.JoinFeatures
>>> j = BOPTools.JoinFeatures.makeConnect(name = 'Connect')
>>> j.Objects = [App.ActiveDocument.SVGFace005, App.ActiveDocument.SVGFace004]
>>> j.Proxy.execute(j)
>>> j.purgeTouched()
>>> for obj in j.ViewObject.Proxy.claimChildren():
>>>     obj.ViewObject.hide()
>>> j = BOPTools.JoinFeatures.makeConnect(name = 'Connect')
>>> j.Objects = [App.ActiveDocument.SVGFace008, App.ActiveDocument.SVGFace007]
>>> j.Proxy.execute(j)
>>> j.purgeTouched()
>>> for obj in j.ViewObject.Proxy.claimChildren():
>>>     obj.ViewObject.hide()
>>> Gui.SendMsgToActiveView("ViewFit")
>>> j = BOPTools.JoinFeatures.makeConnect(name = 'Connect')
>>> j.Objects = [App.ActiveDocument.SVGFace002, App.ActiveDocument.SVGFace001]
>>> j.Proxy.execute(j)
>>> j.purgeTouched()
>>> for obj in j.ViewObject.Proxy.claimChildren():
>>>     obj.ViewObject.hide()
>>> j = BOPTools.JoinFeatures.makeConnect(name = 'Connect')
>>> j.Objects = [App.ActiveDocument.SVGFace003, App.ActiveDocument.Connect002]
>>> j.Proxy.execute(j)
>>> j.purgeTouched()
>>> for obj in j.ViewObject.Proxy.claimChildren():
>>>     obj.ViewObject.hide()
>>> j = BOPTools.JoinFeatures.makeConnect(name = 'Connect')
>>> j.Objects = [App.ActiveDocument.SVGFace006, App.ActiveDocument.SVGFace009]
>>> j.Proxy.execute(j)
>>> j.purgeTouched()
>>> for obj in j.ViewObject.Proxy.claimChildren():
>>>     obj.ViewObject.hide()
>>> j = BOPTools.JoinFeatures.makeConnect(name = 'Connect')
>>> j.Objects = [App.ActiveDocument.SVGFace, App.ActiveDocument.SVGFace012]
>>> j.Proxy.execute(j)
>>> j.purgeTouched()
>>> for obj in j.ViewObject.Proxy.claimChildren():
>>>     obj.ViewObject.hide()
>>> j = BOPTools.JoinFeatures.makeConnect(name = 'Connect')
>>> j.Objects = [App.ActiveDocument.SVGFace011, App.ActiveDocument.SVGFace010]
>>> j.Proxy.execute(j)
>>> j.purgeTouched()
>>> for obj in j.ViewObject.Proxy.claimChildren():
>>>     obj.ViewObject.hide()
>>> j = BOPTools.JoinFeatures.makeConnect(name = 'Connect')
>>> j.Objects = [App.ActiveDocument.Connect006, App.ActiveDocument.Connect, App.ActiveDocument.Connect005, App.ActiveDocument.Connect003, App.ActiveDocument.Connect004, App.ActiveDocument.Connect001]
>>> j.Proxy.execute(j)
>>> j.purgeTouched()
>>> for obj in j.ViewObject.Proxy.claimChildren():
>>>     obj.ViewObject.hide()
>>> App.ActiveDocument.addObject('Part::Feature','Connect007').Shape=App.ActiveDocument.Connect007.Shape.removeSplitter()
>>> App.ActiveDocument.ActiveObject.Label=App.ActiveDocument.Connect007.Label
>>> Gui.ActiveDocument.Connect007.hide()
>>> 
>>> Gui.ActiveDocument.ActiveObject.ShapeColor=Gui.ActiveDocument.Connect007.ShapeColor
>>> Gui.ActiveDocument.ActiveObject.LineColor=Gui.ActiveDocument.Connect007.LineColor
>>> Gui.ActiveDocument.ActiveObject.PointColor=Gui.ActiveDocument.Connect007.PointColor
>>> App.ActiveDocument.recompute()

\>>> f = FreeCAD.getDocument('shape_test').addObject('Part::Extrusion', 'Extrude')
>>> f = App.getDocument('shape_test').getObject('Extrude')
>>> f.Base = App.getDocument('shape_test').getObject('Connect007')
>>> f.DirMode = "Normal"
>>> f.DirLink = None
>>> f.LengthFwd = -0.325000000000000
>>> f.LengthRev = 0.000000000000000
>>> f.Solid = False
>>> f.Reversed = False
>>> f.Symmetric = False
>>> f.TaperAngle = 0.000000000000000
>>> f.TaperAngleRev = 0.000000000000000
>>> Gui.ActiveDocument.Extrude.ShapeColor=Gui.ActiveDocument.Connect007.ShapeColor
>>> Gui.ActiveDocument.Extrude.LineColor=Gui.ActiveDocument.Connect007.LineColor
>>> Gui.ActiveDocument.Extrude.PointColor=Gui.ActiveDocument.Connect007.PointColor
>>> f.Base.ViewObject.hide()
>>> App.ActiveDocument.recompute()
>>> Gui.SendMsgToActiveView("ViewFit")
>>> App.ActiveDocument.addObject('Part::Feature','Extrude').Shape=App.ActiveDocument.Extrude.Shape.removeSplitter()
>>> App.ActiveDocument.ActiveObject.Label=App.ActiveDocument.Extrude.Label
>>> Gui.ActiveDocument.Extrude.hide()
>>> 
>>> Gui.ActiveDocument.ActiveObject.ShapeColor=Gui.ActiveDocument.Extrude.ShapeColor
>>> Gui.ActiveDocument.ActiveObject.LineColor=Gui.ActiveDocument.Extrude.LineColor
>>> Gui.ActiveDocument.ActiveObject.PointColor=Gui.ActiveDocument.Extrude.PointColor
>>> App.ActiveDocument.recompute()
>>> f = FreeCAD.getDocument('shape_test').addObject('Part::Extrusion', 'Extrude')
>>> f = App.getDocument('shape_test').getObject('Extrude')
>>> f.Base = App.getDocument('shape_test').getObject('Connect007001')
>>> f.DirMode = "Normal"
>>> f.DirLink = None
>>> f.LengthFwd = -0.325000000000000
>>> f.LengthRev = 0.000000000000000
>>> f.Solid = False
>>> f.Reversed = False
>>> f.Symmetric = False
>>> f.TaperAngle = 0.000000000000000
>>> f.TaperAngleRev = 0.000000000000000
>>> Gui.ActiveDocument.Extrude.ShapeColor=Gui.ActiveDocument.Connect007001.ShapeColor
>>> Gui.ActiveDocument.Extrude.LineColor=Gui.ActiveDocument.Connect007001.LineColor
>>> Gui.ActiveDocument.Extrude.PointColor=Gui.ActiveDocument.Connect007001.PointColor
>>> f.Base.ViewObject.hide()
>>> App.ActiveDocument.recompute()
>>> f = FreeCAD.getDocument('shape_test').addObject('Part::Extrusion', 'Extrude001')
>>> f = App.getDocument('shape_test').getObject('Extrude001')
>>> f.Base = App.getDocument('shape_test').getObject('Connect007001')
>>> f.DirMode = "Normal"
>>> f.DirLink = None
>>> f.LengthFwd = -0.325000000000000
>>> f.LengthRev = 0.000000000000000
>>> f.Solid = False
>>> f.Reversed = False
>>> f.Symmetric = False
>>> f.TaperAngle = 0.000000000000000
>>> f.TaperAngleRev = 0.000000000000000
>>> Gui.ActiveDocument.Extrude001.ShapeColor=Gui.ActiveDocument.Connect007001.ShapeColor
>>> Gui.ActiveDocument.Extrude001.LineColor=Gui.ActiveDocument.Connect007001.LineColor
>>> Gui.ActiveDocument.Extrude001.PointColor=Gui.ActiveDocument.Connect007001.PointColor
>>> f.Base.ViewObject.hide()
>>> App.ActiveDocument.recompute()
>>> __objs__=[]
>>> __objs__.append(FreeCAD.getDocument("shape_test").getObject("Extrude"))
>>> import ImportGui
>>> ImportGui.export(__objs__,u"/Users/krishna/Downloads/flow_step.step")
>>> 
>>> del __objs__
>>> 
```