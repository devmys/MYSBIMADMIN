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
def collect_levels():
  collector = DB.FilteredElementCollector(doc)
  collector.OfCategory(DB.BuiltInCategory.OST_Levels)
  collector.WhereElementIsNotElementType()
  levelsElements = collector.ToElements()
  levels = []
  for e in levels:
    levels.append([e.Name,e.Elevation,e])
  return levels
#
from pyrevit import forms
#items = ['item1', 'item2', 'item3']
#res = forms.SelectFromList.show(items, button_name='Select Item',multiselect=True)
#        >>> ['item1']
#        >>> ops = [viewsheet1, viewsheet2, viewsheet3]
#        >>> res = forms.SelectFromList.show(ops, multiselect=Falsename_attr='Name',
ops = {'Sheet Set A': ['viewsheet1', 'viewsheet2', 'viewsheet3'],'Sheet Set B': ['viewsheet4', 'viewsheet5', 'viewsheet6']}
res = forms.SelectFromList.show(ops, multiselect=True, group_selector_title='Sheet Sets',button_name='Select Sheets')
print(res)
levels = collect_levels()
print(levels)
# for timing -------------------------------------------------------------------
#endtime = timer.get_time()
#print(endtime)
# ------------------------------------------------------------------------------


