__doc__ = """Advanced Collection of Data: Collects all the walls of height 10"""
#
# for timing -------------------------------------------------------------------
from pyrevit.coreutils import Timer
timer = Timer()
# ------------------------------------------------------------------------------
import Autodesk.Revit.DB as DB
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument
# ------------------------------------------------------------------------------
def collect_CurtainWallTypes():
  collector = DB.FilteredElementCollector(doc)
  collector.OfCategory(DB.BuiltInCategory.OST_Walls)
  collector.WhereElementIsElementType()
  wallTypes = collector.ToElements()
  curtainWallTypes  = []
  for wt in wallTypes:
    if wt.Kind.ToString()=='Curtain':
      curtainWallTypes.append(wt.Id)
  return curtainWallTypes
#----------------------------------------------------------
def collect_CurtainWalls():
  cwTypes = collect_CurtainWallTypes()
  collector = DB.FilteredElementCollector(doc)
  collector.OfCategory(DB.BuiltInCategory.OST_Walls)
  collector.WhereElementIsNotElementType()
  walls = collector.ToElements()
  CurtainWalls = []
  for wall in walls:
    if cwTypes.Contains(wall.WallType):
      CurtainWalls.append(wall)
  return CurtainWalls

#----------------------------------------------------------

def main():
  print("Running main")
  cw = collect_CurtainWalls()
  print("There are {} Curtian Walls".format(len(cw)))
#----------------------------------------------------------
if __name__ == "__main__":
    main()
else:
  print("not")

