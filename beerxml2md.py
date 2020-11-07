import sys
import os
from xml.etree import ElementTree as ET

if len(sys.argv) != 2:
    exit("Incorrect number of arguments")

filename = sys.argv[1]
EOL = os.linesep

def setTableHeaders(headers: list ) -> str:
    """ Generate a table hader based on a given list """
    output = "| " + " | ".join(headers) + " |" + EOL
    ii = 0
    while ii < len(headers):
        output += "| --- "
        ii += 1
    output += "|" + EOL
    return output 

def setTableRow( recipe, elementName: str, label: str, unit: str = "" ):
    """ generate a table row based on an element name """
    output = "| " + label + " | "
    output += recipe.findtext(elementName, "")

    output += " | " + unit + " |" + EOL
    return output

def getRecipeTitle(recipe) -> str:
    """ Generate a H1 title for the note containing  the recipe name """
    return "# "  + recipe.find("NAME").text + EOL + EOL

def getRecipeNotes(recipe) -> str:
    """ Put the recipe notes in paragraphs"""
    output = recipe.findtext("NOTES","") 
    if len(output) > 0:
        output += EOL + EOL
    return output


def getGeneralData(recipe) -> str:
    """ Generate a table containing the general recipe data """

    output = "## Basisgegevens" + EOL + EOL
    output += setTableHeaders(["Omschrijving", "Waarde", "Eenheid"])
    output += setTableRow(recipe, "NAME", "Naam recept", "")
    output += "| Kenmerk | | |" + EOL
    output += setTableRow(recipe, "DATE", "Brouwdatum", "")
    style = recipe.find("STYLE")
    output += setTableRow(style, "NAME", "Bierstijl", "")
    output += setTableRow(recipe, "BATCH_SIZE", "Volume", "l")
    output += setTableRow(recipe,"EST_COLOR", "Kleur", "")
    output += setTableRow(recipe, "IBU", "Bitterheid", "Rager")
    output += setTableRow(recipe, "EFFICIENCY", "Brouwzaalrendement", "%")
    output += setTableRow(recipe, "BOIL_TIME", "Kooktijd", "min")

    output += EOL
    return output    

def getWater(recipe) -> str:
    """ Generate table concerning water for maisching and sparging """
    output = "## Water" + EOL + EOL
    output += setTableHeaders(["", "Volume", "Eenheid"])
    output += "| Maischwater | | l |" + EOL #TODO
    output += "| Spoelwater | | l |" + EOL + EOL

    return output

def getWaterProfile(recipe) -> str:
    """ If applicable, generate a table containing a water profile """
    water = recipe.find("./WATERS/WATER")
    if(water == None):
        return ""
    output = "## Waterprofiel" + EOL + EOL
    output += setTableHeaders(["Ca", "Mg", "Na", "HCO3", "Cl", "SO4", "PH"])
    output += "|"
    for prop in ["CALCIUM", "MAGNESIUM", "SODIUM", "", "CHLORIDE", "SULFATE", "PH"]:
        value = round(float(water.findtext(prop,0)),1)
        output += " " + str(value) + " | "
    output += EOL + EOL

    return output
# 
def getFermentables(recipe) -> str:
    """ Generate a table with fermentable ingredients """
    output = "## Vergistbare ingrediënten" + EOL + EOL
    output += setTableHeaders(["Hoeveelheid", "Naam", "Mouterij", "Kleur", "Percentage"])
    for f in recipe.findall("./FERMENTABLES/FERMENTABLE"):
        line = "| " + f.findtext("DISPLAY_AMOUNT", "") + " | "
        line += f.findtext("NAME", "") + " | " + f.findtext("SUPPLIER", "")
        line += " | " + f.findtext("DISPLAY_COLOR", "") + " | |" + EOL
        output += line
    output += EOL
    return output 

def getMiscIngredients(recipe) -> str:
    """ Renerate a table with miscellaneous ingredients (spices, sugar, ...) """
    miscs = recipe.findall("./MISCS/MISC")
    if(len(miscs) > 0):
        output = "## Overige ingrediënten" + EOL + EOL
        output += setTableHeaders(["Naam", "Hoeveelheid", "Kooktijd"])
        for mm in miscs:
            output += "| " + mm.findtext("NAME") + " | "
            output += mm.findtext("DISPLAY_AMOUNT","") + " | "
            output += mm.findtext("DISPLAY_TIME", "") + " |" + EOL
        return output + EOL + EOL
    return ""

def getMashingScheme(recipe) -> str:
    """ Generate a table with the mashing scheme """
    output = "## Maischschema" + EOL + EOL
    output += setTableHeaders(["Omschrijving", "Temperatuur", "Staptijd", "Rusttijd", "Beslagdikte"])
    for step in recipe.findall("./MASH/MASH_STEPS/MASH_STEP"):
        output += "| " + step.findtext("NAME", step.findtext("TYPE","")) + " | "
        output += step.findtext("DISPLAY_STEP_TEMP", "") + " | "
        stepTime = step.findtext("STEP_TIME","")
        if stepTime.isnumeric():
            output += str(round(float(step.findtext("STEP_TIME", 0))))
        else:
            output += stepTime
        output += " | " +str(round(float(step.findtext("RAMP_TIME", 0)))) + " | "
        output += step.findtext("WATER_GRAIN_RATIO","") + " |" + EOL
    return output + EOL + EOL

def getHops(recipe) -> str:
    """ Generate a table with hop scheme """
    output = "## Hopgiftschema" + EOL + EOL
    output += setTableHeaders(["Naam", "Hoeveelheid", "Kookijd", "Vorm", "Alfazuur %", "Betazuur %", "IBU %"])
    for hop in recipe.findall("./HOPS/HOP"):
        output += "| " + hop.findtext("NAME") + " | " 
        output += hop.findtext("DISPLAY_AMOUNT", str(( 1000 * float(hop.findtext("AMOUNT",0))))) + " | "
        output += hop.findtext("DISPLAY_TIME", hop.findtext("TIME",0)) + " | "
        output += hop.findtext("FORM", "") + " | "
        output += str(round(float(hop.findtext("ALPHA",0)),1)) + " | "
        output += str(round(float(hop.findtext("BETA",0)),1)) + " | |" + EOL

    return output + EOL + EOL

def getYeasts(recipe) -> str:
    """ Generate a table for yeast data """
    output = "## Gistschema" + EOL + EOL
    output += setTableHeaders(["Hoeveelheid", "Naam", "Type"])
    for yeast in recipe.findall("./YEASTS/YEAST"):
        output += "| " + yeast.findtext("DISPLAY_AMOUNT", str(1000 * float(yeast.findtext("AMOUNT",0)))) + " | "
        output += yeast.findtext("NAME", "") + " " + yeast.findtext("LABORATORY", "")
        output += " " +yeast.findtext("PRODUCT_ID", "") + " | "
        output += yeast.findtext("TYPE", "") + " |"
    return output + EOL + EOL

def xml2md(DOMTree) -> str:
    """ Generate a markdown string from a BeerXML file """
    recipe = DOMTree.find("RECIPE")
    output = getRecipeTitle(recipe) + getRecipeNotes(recipe) 
    output += getGeneralData(recipe)
    output += getWater(recipe)
    output += getWaterProfile(recipe)
    output += getFermentables(recipe)
    output += getMiscIngredients(recipe)
    output += getMashingScheme(recipe)
    output += getHops(recipe)
    output += getYeasts(recipe)

    return output

try:
    with open(filename, 'r') as f:
        DOMTree = ET.parse(f).getroot()
        strMdOutput = xml2md(DOMTree)
        basename = os.path.basename(filename)
        f_name, f_ext = os.path.splitext(basename)
        ff = open(f_name+".md", "w")
        ff.write(strMdOutput)
        ff.close()
except IOError:
    exit(filename + " not accesable")
