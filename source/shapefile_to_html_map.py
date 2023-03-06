"""Ice Climatology Shapefile to HTML Map Generator

This module provides tools for converting different CIS ice climatology shapefiles into interactive HTML maps that can be loaded into the main GUI.
"""
import geopandas as gpd

def bucketIceConcentration(mapDataFrame,concentrationVariable):
    """Bucket median ice concentration into the appropriate categories

    Args:
        mapDataFrame (geopandas): A geopandas dataframe representation of a CIS combined ice climatology shapefile.
        concentrationVariable (str): Either 'cpmed' or 'ctmed'; the string name of the ice concentation column

    Returns:
        list: An array of ice concentration category values of equal length to the original input.
    """
    result = []
    for value in mapDataFrame[concentrationVariable]:
        if value == None:
            result.append('No data')
        elif value == 'X':
            result.append('X')
        elif value == 'L':
            result.append('Land')
        elif value == '10' or value == '20' or value == '30':
            result.append("1 - 3/10")
        elif value == '40' or value == '50' or value == '60':
            result.append("4 - 6/10")
        elif value == '70' or value == '80':
            result.append("7 - 8/10")
        elif value == '90' or value == '91':
            result.append("9 - 9+/10")
        elif value == '92':
            result.append("10/10")
        else:
            result.append("Less than 1/10")

    return result

def bucketIceType(mapDataFrame,iceTypeVariable):
    """Bucket predominant ice type into the appropriate categories

    Args:
        mapDataFrame (geopandas): A geopandas dataframe representation of a CIS combined ice climatology shapefile.
        iceTypeVariable (str): Either 'pimed' or 'prmed'; the string representing the ice type column

    Returns:
        list: An array of predominant ice type category values of equal length to the original input.
    """
    result = []
    for value in mapDataFrame[iceTypeVariable]:
        if value == None:
            result.append('No data')
        elif value == 'X':
            result.append('X')
        elif value == 'L':
            result.append('Land')
        elif value == '01':
            result.append("Ice Free")
        elif value == '81':
            result.append("New Lake Ice")
        elif value == '84':
            result.append("Thin Lake Ice")
        elif value == '85' or value == '91':
            result.append("Medium Lake Ice")
        elif value == '87':
            result.append("Thick Lake Ice")
        else:
            result.append("Very Thick Lake Ice")

    return result

def bucketIceFrequency(mapDataFrame):
    """Bucket frequency of presence of ice into the appropriate categories

    Args:
        mapDataFrame (geopandas): A geopandas dataframe representation of a CIS combined ice climatology shapefile.

    Returns:
        list: An array of ice frequency category values of equal length to the original input.
    """
    result = []
    for value in mapDataFrame["icfrq"]:
        if value == None or int(value) == '-1':
            result.append('No data')
        elif float(value) < 0.01: # less than 1%
            result.append('0 - 1%')
        elif float(value) < 0.04:
            result.append('1 - 4%')
        elif float(value) < 0.17:
            result.append("4 - 17%")
        elif float(value) < 0.34:
            result.append("17 - 34%")
        elif float(value) < 0.50:
            result.append("34 - 50%")
        elif float(value) < 0.67:
            result.append("50 - 67%")
        elif float(value) < 0.83:
            result.append("67 - 83%")
        elif float(value) < 0.97:
            result.append("83 - 97%")
        else:
            result.append("97 - 100%")
    
    return result

def determineDisplayColorMap(mapDisplayVariable):
    """Determine which color scheme to use based on the map's displayed variable.

    Args:
        mapDisplayVariable (str): One of ctmed, cpmed, icfrq, pimed, or prmed. The variable to display on the map.

    Returns:
        list: A list of mapplotlib colors (strings).
    """
    if mapDisplayVariable == "ctmed" or mapDisplayVariable == "cpmed":
        # median concentration
        return ['lightskyblue','springgreen','yellow','orange','red','darkgrey','white']
    elif mapDisplayVariable == "pimed" or mapDisplayVariable == "prmed":
        # predominant ice type
        return ['lightskyblue', 'thistle', 'mediumorchid', 'magenta', 'greenyellow', 'limegreen', 'white']
    else:
        # ice frequency
        return ['lightskyblue','yellow', 'gold', 'orange', 'deeppink', 'magenta', 'blue', 'navy', 'darkgrey', 'white']

def determineDisplayCategories(mapDisplayVariable):
    """Determine which named categories to use based on the map's displayed variable.

    Args:
        mapDisplayVariable (str): One of ctmed, cpmed, icfrq, pimed, or prmed. The variable to display on the map.

    Returns:
        list: A list of category names for the map.
    """
    if mapDisplayVariable == "ctmed" or mapDisplayVariable == "cpmed":
        # median concentration
        return ['Less than 1/10','1 - 3/10', '4 - 6/10', '7 - 8/10', '9 - 9+/10', '10/10', 'No data']
    elif mapDisplayVariable == "pimed" or mapDisplayVariable == "prmed":
        # predominant ice type
        return ['Ice Free', 'New Lake Ice', 'Thin Lake Ice', 'Medium Lake Ice', 'Thick Lake Ice', 'Very Thick Lake Ice', 'No data']
    else:
        # ice frequency
        return ['0 - 1%','1 - 4%', '4 - 17%', '17 - 34%', '34 - 50%', '50 - 67%', '67 - 83%', '83 - 97%', '97 - 100%', 'No data']

def determineDisplayAliases(mapDisplayVariable):
    """Determine the alias, aka human friendly name, for this display variable

    Args:
        mapDisplayVariable (str): One of ctmed, cpmed, icfrq, pimed, or prmed. The variable to display on the map.

    Returns:
        list: A list of strings of length 1.
    """
    if mapDisplayVariable == 'ctmed':
        return ['Median Ice Concentration']
    elif mapDisplayVariable == 'cpmed':
        return ['Median Ice Concentration when Ice Present']
    elif mapDisplayVariable == 'icfrq':
        return ['Frequency of Presence of Ice']
    elif mapDisplayVariable == 'pimed':
        return ['Median Predominant Ice Type']
    else:
        return ['Median Predominant Ice Type when Ice is Present']

def preprocessMapShapefile(mapDataFrame):
    """Perform some preprocessing on the map shapefile. Bucket each variable into the appropriate categories and remove the land and 'X' polygons for the display.

    Args:
        mapDataFrame (geopandas): A geopandas dataframe representation of a CIS combined ice climatology shapefile.

    Returns:
        geopandas: A geopandas dataframe representation of a CIS combined ice climatology shapefile with additional columns.
    """
    # bucket concentrations
    mapDataFrame["cpmed_proc"] = bucketIceConcentration(mapDataFrame,"cpmed")
    mapDataFrame["ctmed_proc"] = bucketIceConcentration(mapDataFrame,"ctmed")  

    # bucket predominant ice types
    mapDataFrame["pimed_proc"] = bucketIceType(mapDataFrame,"pimed")
    mapDataFrame["prmed_proc"] = bucketIceType(mapDataFrame,"prmed")

    # bucket ice frequency
    mapDataFrame["icfrq_proc"] = bucketIceFrequency(mapDataFrame)

    # remove land and X from the polygons
    mapDataFrame.query("ctmed != 'L'",inplace=True)
    mapDataFrame.query("ctmed != 'X'",inplace=True)

    return mapDataFrame

def preprocessIndividualMapShapefile(mapDataFrame,mapDisplayVariable):
    """Perform some preprocessing on the map shapefile. Bucket each variable into the appropriate categories and remove the land and 'X' polygons for the display.

    Args:
        mapDataFrame (geopandas): A geopandas dataframe representation of a CIS combined ice climatology shapefile.

    Returns:
        geopandas: A geopandas dataframe representation of a CIS combined ice climatology shapefile with additional columns.
    """
    if mapDisplayVariable == "cpmed":
        # bucket concentrations
        mapDataFrame["cpmed_proc"] = bucketIceConcentration(mapDataFrame,"cpmed")
    elif mapDisplayVariable == "ctmed":
        mapDataFrame["ctmed_proc"] = bucketIceConcentration(mapDataFrame,"ctmed")
    elif mapDisplayVariable == "pimed":
        # bucket predominant ice types
        mapDataFrame["pimed_proc"] = bucketIceType(mapDataFrame,"pimed")
    elif mapDisplayVariable == "prmed":
        mapDataFrame["prmed_proc"] = bucketIceType(mapDataFrame,"prmed") 
    else:
        # ice frequency
        mapDataFrame["icfrq_proc"] = bucketIceFrequency(mapDataFrame)

    # remove land and X from the polygons
    if mapDisplayVariable == "icfrq":
        mapDataFrame.query("icfrq != -1",inplace=True)
    else:
        mapDataFrame.query(mapDisplayVariable+" != 'L'",inplace=True)
        mapDataFrame.query(mapDisplayVariable+" != 'X'",inplace=True)

    return mapDataFrame

def createCombinedIceMap(mapFilePath,mapDateString,mapDisplayVariable):
    """Generate an interactive HTML map from a combined CIS shapefile.

    Args:
        mapFilePath (str): Relative filepath to the CIS shapefile.
        mapDateString (str): Four character string indicating the month and week of the shapefile data (e.g. '0108').
        mapDisplayVariable (str): which of the ice climatologies variables to display

    Returns:
        str: The name of the generated html map file.
    """
    mapDataFrame = preprocessMapShapefile(gpd.read_file(mapFilePath))

    displayColorMap = determineDisplayColorMap(mapDisplayVariable)
    displayCategories = determineDisplayCategories(mapDisplayVariable)
    legendDisplayAliases = determineDisplayAliases(mapDisplayVariable)
    popupDisplayAliases = ['Median Ice Concentration','Median Ice Concentration when Ice Present','Frequency of Presence of Ice','Median Predominant Ice Type','Median Predominant Ice Type when Ice is Present']

    iceMap = mapDataFrame.explore(
        column=mapDisplayVariable+"_proc", # color by concentration column
        tooltip=mapDisplayVariable+"_proc", # show "concentration" value in tooltip (on hover)
        popup=['ctmed_proc','cpmed_proc','icfrq_proc','pimed_proc','prmed_proc'], # show these values in popup (on click)
        tiles="CartoDB positron", # use "CartoDB positron" tiles
        cmap=displayColorMap, # use custom colormap
        categories=displayCategories, # custom categories
        style_kwds=dict(weight=1,opacity=0.3,fillOpacity=0.75), # use thin outline
        highlight_kwds=dict(fillOpacity=1),
        tooltip_kwds=dict(labels=False),
        popup_kwds=dict(aliases=popupDisplayAliases),
        legend_kwds=dict(caption=legendDisplayAliases[0])
    )

    # save map as html and load it back in
    short_url = mapDisplayVariable+"_"+mapDateString+".html"
    url = "./data/tmp_maps/combined/"+short_url
    iceMap.save(url)

    return short_url

def createIndividualIceMap(mapFilePath,mapDateString,mapDisplayVariable):
    """Generate an interactive HTML map from a combined CIS shapefile.

    Args:
        mapFilePath (str): Relative filepath to the CIS shapefile.
        mapDateString (str): Four character string indicating the month and week of the shapefile data (e.g. '0108').
        mapDisplayVariable (str): which of the ice climatologies variables to display

    Returns:
        str: The name of the generated html map file.
    """
    mapDataFrame = preprocessIndividualMapShapefile(gpd.read_file(mapFilePath),mapDisplayVariable)

    displayColorMap = determineDisplayColorMap(mapDisplayVariable)
    displayCategories = determineDisplayCategories(mapDisplayVariable)
    displayVariableAliases = determineDisplayAliases(mapDisplayVariable)
    
    iceMap = mapDataFrame.explore(
        column=mapDisplayVariable+"_proc", # color by concentration column
        tooltip=mapDisplayVariable+"_proc", # show "concentration" value in tooltip (on hover)
        popup=[mapDisplayVariable+"_proc"], # show these values in popup (on click)
        tiles="CartoDB positron", # use "CartoDB positron" tiles
        cmap=displayColorMap, # use custom colormap
        categories=displayCategories, # custom categories
        style_kwds=dict(weight=1,opacity=0.3,fillOpacity=0.75), # use thin outline
        highlight_kwds=dict(fillOpacity=1),
        tooltip_kwds=dict(labels=False),
        popup_kwds=dict(aliases=displayVariableAliases),
        legend_kwds=dict(caption=displayVariableAliases[0])
    )

    # save map as html and load it back in
    short_url = mapDisplayVariable+"_"+mapDateString+".html"
    url = "./data/tmp_maps/"+mapDisplayVariable+"/"+short_url
    iceMap.save(url)

    return short_url

def createMap(mapFilePath,mapDateString,mapVariable,mapShapefileState):
    """Generate an interactive HTML map for a given ice climatology variable CIS shapefile.

    Args:
        mapFilePath (str): Relative filepath to the CIS shapefile.
        mapDateString (str): Four character string indicating the month and week of the shapefile data (e.g. '0108').
        mapVariable (str): One of 'ctmed', 'cpmed', 'icfrq', 'pimed', or 'prmed'

    Returns:
        str: The name of the generated html map file.
    """
    if mapShapefileState == "Combined":
        return createCombinedIceMap(mapFilePath, mapDateString, mapVariable)
    else:
        return createIndividualIceMap(mapFilePath, mapDateString, mapVariable)