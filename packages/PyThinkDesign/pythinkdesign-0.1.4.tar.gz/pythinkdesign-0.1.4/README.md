# PyThinkDesign

python sdk for thinkdesign

## install

```bash
pip install PyThinkDesign
```

## usage

### 1. Get or Create TD application
if the TD application is not running, it will be created.

```python
from PyThinkDesign import Application
app = Application.GetOrCreateApplication()
``` 

### 2. Create lines and arcs in a document

```python
import Application
import Geo3d

# get application and document
app = Application.GetOrCreateApplication()
doc = app.ActiveDocument

# get creators
curveCreator = doc.CurveCreator

#add lines
p1 = Geo3d.Point(0,0,0)
p2 = Geo3d.Point(1,0,0)
p3 = Geo3d.Point(1,1,0)
p4 = Geo3d.Point(0,1,0)
curveCreator.AddLine(p1,p2)
curveCreator.AddLine(p2,p3)
curveCreator.AddLine(p3,p4)
curveCreator.AddLine(p4,p1)

#add arc
pCenter = Geo3d.Point(10,0,0)
pXDir = Geo3d.Vector(1,0,0)
pYDir = Geo3d.Vector(0,1,0) 
radius = 10
startAng = 0
endAng = 60
curveCreator.AddArc(pCenter, pXDir, pYDir, radius, startAng, endAng)

#doc.SaveAs("d:\\tdApp.e3")
app.Quit()
```



