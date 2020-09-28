from Autodesk.Revit import DB
from Autodesk.Revit.DB import *
# ------------------------------
from pyrevit import forms
doc = __revit__.ActiveUIDocument.Document


import sys

from rpw.ui.forms.flexform import FlexForm, Label, ComboBox, TextBox, Button
#------------------------------
def toInternalUnits(val):
	docUnitLength = Document.GetUnits(doc).GetFormatOptions(UnitType.UT_Length).DisplayUnits
	return UnitUtils.ConvertToInternalUnits(val,docUnitLength)
#------------------------------
def todDocUnits(val):
	docUnitLength = Document.GetUnits(doc).GetFormatOptions(UnitType.UT_Length).DisplayUnits
	return UnitUtils.c
#------------------------------
def jt_FromIntUnits(lengthValue ):
	return UnitUtils.ConvertFromInternalUnits(lengthValue,Document.GetUnits(doc).GetFormatOptions(UnitType.UT_Length).DisplayUnits)
def jt_toInternalUnits(lengthValue):
	return UnitUtils.ConvertToInternalUnits(lengthValue,Document.GetUnits(doc).GetFormatOptions(UnitType.UT_Length).DisplayUnits)
#------------------------------
def collect_level_elements():
    levels_collector = DB.FilteredElementCollector(doc)
    levels_collector.OfCategory(DB.BuiltInCategory.OST_Levels)
    levels_collector.WhereElementIsNotElementType()
    return_elements =list(levels_collector.ToElements())
    return return_elements
#------------------------------
def collect_level_info():
# Creating collector instance and collecting all levels from the model, sorting by elevation
    rdata = []
    gf = []
    levels_above_gf=[]
    levels_below_gf=[]
    ##
    levels_collector = DB.FilteredElementCollector(doc)
    levels_collector.OfCategory(DB.BuiltInCategory.OST_Levels)
    levels_collector.WhereElementIsNotElementType()
    #
    for level in levels_collector:
        elevation = round(jt_FromIntUnits(level.Elevation),6)
        name = level.Name
        if (elevation == 0.0):
            gf.append([name,elevation])
        elif (elevation > 0.0):
            levels_above_gf.append([name,elevation])
        else:
            levels_below_gf.append([name,elevation])
    return levels_below_gf,gf,levels_above_gf
#------------------------------
def rename_above_gf_levels(levels):
    sorted_levels = sorted(levels , key = lambda x: x[1])
    level_names = []
    for index,level in enumerate(sorted_levels,1):
        newLevel = 'F-' + str(index).zfill(2)
        level_names.append([level[0],newLevel])
    return level_names
#------------------------------
def rename_below_gf_levels(levels):
    sorted_levels = sorted(levels , key = lambda x: x[1])
    sorted_levels.reverse()
    level_names = []
    for index,level in enumerate(sorted_levels,1):
        newLevel = 'B-' + str(index).zfill(2)
        level_names.append([level[0],newLevel])
    return level_names
#------------------------------
def get_levels_to_skip(levels):
    ops = []
    for level in levels:
        ops.append(level)
    res = forms.SelectFromList.show(ops, multiselect=True, name_attr='Name',  button_name='Select Levels to Skip') 
    return list(res)
#------------------------------
def get_mez_levels(levels):
    ops = []
    for level in levels:
        ops.append(level)
    res = forms.SelectFromList.show(ops, multiselect=True, name_attr='Name',  button_name='Select Mezzanine/Gallery Levels') 
    return list(res)
#------------------------------
def LevelRename(newNames):
    for x in newNames:
        print ("{} is going to change to \t{}\t\t at Elevation {}".format(x[0].Name,x[1],round(jt_FromIntUnits(x[0].Elevation),4)))
    t = Transaction(doc,"Renaming Levels")
    t.Start()
    for x in newNames:
        x[0].Name = x[1]
    t.Commit()
#------------------------------
def select_views_with_associated_levels ():
    views_collector = DB.FilteredElementCollector(doc)
    views_collector.OfCategory(DB.BuiltInCategory.OST_Views)
    views_collector.WhereElementIsNotElementType()
    views_list = views_collector.ToElements()
    view_with_levels = []
    for v in views_list:
        if (v.LookupParameter('Associated Level') != None ):
            view_with_levels.append([v , v.LookupParameter('Associated Level').AsString()])
    return view_with_levels
#------------------------------
def group_view_by_type(lo_views):
    returnData = {}
    lo_vt = map(lambda x: x.__str__(), list(set(map (lambda x: x.ViewType ,lo_views))))
    for x in lo_vt:
        returnData[x] = []
    for v in lo_views:
         returnData[v.ViewType.__str__()].append(v)
    return returnData
#------------------------------
def group_view_by_template(lo_views):
    returnData = {}
    lo_vtm = map(lambda x: x.__str__(), list(set(map (lambda x: x.ViewTemplateId ,lo_views))))
    for x in lo_vtm:
        returnData[x] = []
    for v in lo_views:
        returnData[v.ViewTemplateId.__str__()].append(v)
    return returnData
#------------------------------
def get_viewName_prefix_byTemplate(templates):
    templatePrefix = []
    for template in templates:
        if int(template) != -1:
            vtn = (doc.GetElement(DB.ElementId(int(template))).Name)
            templatePrefix.append(vtn.replace(" ","-"))
        else :
            templatePrefix.append("No-Template")
    
    res = MultipleTextInput("Add view prefix according to template :", templatePrefix )
    return list(res)
#------------------------------
def MultipleTextInput(title, buttonNamesValues , default=None, description=None, sort=True, exit_on_close=True ,  ):
  components = []
  rvalues = []
  for b in buttonNamesValues:
    
    label = Label("Template_"+ b)
    textbox = TextBox(b, default=b )
    components.append(label)
    components.append(textbox)
    rvalues.append(b)
  components.append(Button('Select'))
  form = FlexForm(title, components)
  ok = form.show()
  if ok:
    a =  []
    for x in buttonNamesValues:
      a.append([x,form.values[x]])
    return a
  if exit_on_close:
    sys.exit()

#------------------------------

def get_levels_newNames():
    levels  = collect_level_elements()
    skip = get_levels_to_skip(levels)
    galeries = get_mez_levels(levels)
    levels.sort(key = lambda x :  round(jt_FromIntUnits(x.Elevation),4))
    gfIndex = -1
    for i,level in enumerate(levels):
        if round(jt_FromIntUnits(level.Elevation) , 3)  == 0.0:
            gfIndex = i
    number_of_below_ground = gfIndex
    newNames = []
    index = 0
    while number_of_below_ground > 0:
        newNames.append([levels[index] , 'B-' + str(number_of_below_ground).zfill(2)])
        number_of_below_ground -= 1
        index +=1
    newNames.append([levels[gfIndex],'GF'])
    index = 0
    for x in levels[gfIndex+1:]:
        if x in galeries:
            if index == 0 :
                newNames.append([x  , 'GF-G'])
            else :
                newNames.append([x  ,  'F-' + str(index).zfill(2) + 'G'])
        else :
                index +=1
                newNames.append([x,'F-'+ str(index).zfill(2)])
    return newNames
#------------------------------
#------------------------------

def mainfunction():
    newNames = get_levels_newNames()
    oldNewNames = {}
    for x in newNames:
        oldNewNames[x[0].Name] = x[1]
    views = select_views_with_associated_levels()
    lo_vbtm = group_view_by_template(map(lambda x: x[0] , views))
    
    #for x in lo_vbtm.keys():
    #    if int(x) != -1:
    #        print (doc.GetElement(DB.ElementId(int(x))).Name)
    #        for v in lo_vbtm[x]:
    #            print '\t\t' + v.Name
    #    else:
    #        print "No Template"
    #        for v in lo_vbtm[x]:
    #            print '\t\t' + v.Name
    print '======================================'
    vt = [k for k in lo_vbtm.keys()]
    vpfx = get_viewName_prefix_byTemplate(vt)
    for x in vpfx:
        print "Views with {} Template are going to be prefixed with {}_".format(x[0],x[1])

    #for x in views:
    #    for k in oldNewNames.keys():
    #        if x[1].find(k) > -1:
    #            print "{} found at {} and is going to be{}".format(k,x[0].Name, x[0].Name.replace(k,oldNewNames[k]))

# -----------------------------
mainfunction()
