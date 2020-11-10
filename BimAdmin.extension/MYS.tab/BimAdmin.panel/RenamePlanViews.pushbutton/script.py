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
def get_view_templates():
    levels_collector = DB.FilteredElementCollector(doc)
    levels_collector.OfCategory(DB.BuiltInCategory.OST_Views)
    levels_collector.WhereElementIsNotElementType()
    views = levels_collector.ToElements()
    viewTemplates = []
    for x in views :
        if (x.IsTemplate):
            viewTemplates.append(x)
    return viewTemplates

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
