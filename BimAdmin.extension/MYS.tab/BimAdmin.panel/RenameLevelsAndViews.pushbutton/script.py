from Autodesk.Revit import DB
from Autodesk.Revit.DB import *
# ------------------------------
from pyrevit import forms
doc = __revit__.ActiveUIDocument.Document
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

def rename_above_gf_levels(levels):
    sorted_levels = sorted(levels , key = lambda x: x[1])
    level_names = []
    for index,level in enumerate(sorted_levels,1):
        newLevel = 'F-' + str(index).zfill(2)
        level_names.append([level[0],newLevel])
    return level_names

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
def mainfunction():
    levels  = collect_level_elements()
    skip = get_levels_to_skip(levels)
    print (dir(levels))
    for x in skip:
        levels.remove(x)
    galeries = get_mez_levels(levels)
    levels.sort(key = lambda x :  round(jt_FromIntUnits(x.Elevation),4))
    print('--------------sorted----------------')
    gfIndex = -1
    for i,level in enumerate(levels):
        if round(jt_FromIntUnits(level.Elevation) , 3)  == 0.0:
            gfIndex = i 
    print('--------------gf----------------')
    gf = levels[gfIndex]
    print('Ground Floor is {}  '.format(gf.Name))
    number_of_below_ground = gfIndex
    index = 0
    newNames = []
    while number_of_below_ground > 0:
        newNames.append([levels[index] , 'B-' + str(number_of_below_ground).zfill(2)])
        number_of_below_ground -= 1
        index +=1
    #------------------------------
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
    for x in newNames:
        print ("{} is going to change to \t{}\t\t at Elevation {}".format(x[0].Name,x[1],round(jt_FromIntUnits(x[0].Elevation),4)))
# -----------------------------
mainfunction()