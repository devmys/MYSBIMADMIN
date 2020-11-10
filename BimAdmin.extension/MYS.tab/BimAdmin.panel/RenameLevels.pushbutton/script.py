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


#------------------------------
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

#------------------------------
def get_levels_newNames():
    levels  = collect_level_elements()
    skip = get_levels_to_skip(levels)
    galeries = get_mez_levels(levels)
    for k in skip:
        levels.remove(k)
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
def mainfunction():
    newNames = get_levels_newNames()
    t = Transaction(doc,"Renaming Levels")
    t.Start()
    for x in newNames:
        x[0].Name = x[1]
    t.Commit()
# -----------------------------
mainfunction()