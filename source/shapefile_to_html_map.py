"""Ice Climatology Shapefile to HTML Map Generator

This module provides tools for converting different CIS ice climatology shapefiles into interactive HTML maps that can be loaded into the main GUI.
"""
import geopandas as gpd

def createIceConcentrationWhenPresentMap(mapFilePath,mapDateString):
    """Generate an interactive HTML map from a median ice concentration when ice is present CIS shapefile.

    Args:
        mapFilePath (str): Relative filepath to the CIS shapefile.
        mapDateString (str): Four character string indicating the month and week of the shapefile data (e.g. '0108').

    Returns:
        str: The name of the generated html map file.
    """
    mapDataFrame = gpd.read_file(mapFilePath)

    # bucket concentrations
    result = []
    for value in mapDataFrame["cpmed"]:
        if value == None or value == 'X':
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
    mapDataFrame["Concentration"] = result  

    # filter out land and unknown polygons
    mapDataFrame.query("cpmed != 'L'",inplace=True)
    mapDataFrame.query("cpmed != 'X'",inplace=True)
    mapDataFrame.query("cpmed != 'None'",inplace=True)

    cisColorMap = ['lightskyblue','springgreen','yellow','orange','red','darkgrey','lightgrey']
    concentrationCategories = ['Less than 1/10','1 - 3/10', '4 - 6/10', '7 - 8/10', '9 - 9+/10', '10/10', 'Undefined']
    
    iceMap = mapDataFrame.explore(
        column="Concentration", # color by concentration column
        tooltip="Concentration", # show "concentration" value in tooltip (on hover)
        popup=True, # show all values in popup (on click)
        tiles="CartoDB positron", # use "CartoDB positron" tiles
        cmap=cisColorMap, # use custom colormap
        categories=concentrationCategories, # custom categories
        style_kwds=dict(color="black") # use black outline
    )

    # save map as html and load it back in
    short_url = "cpmed_"+mapDateString+".html"
    url = "./data/tmp_maps/cpmed/"+short_url
    iceMap.save(url)

    return short_url

def createIceConcentrationMap(mapFilePath,mapDateString):
    """Generate an interactive HTML map from a median ice concentration CIS shapefile.

    Args:
        mapFilePath (str): Relative filepath to the CIS shapefile.
        mapDateString (str): Four character string indicating the month and week of the shapefile data (e.g. '0108').

    Returns:
        str: The name of the generated html map file.
    """
    mapDataFrame = gpd.read_file(mapFilePath)
    
    # bucket concentrations
    result = []
    for value in mapDataFrame["ctmed"]:
        if value == None or value == 'X':
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
    mapDataFrame["Concentration"] = result  

    # filter out land and unknown polygons
    mapDataFrame.query("ctmed != 'L'",inplace=True)
    mapDataFrame.query("ctmed != 'X'",inplace=True)
    mapDataFrame.query("ctmed != 'None'",inplace=True)

    cisColorMap = ['lightskyblue','springgreen','yellow','orange','red','darkgrey','lightgrey']
    concentrationCategories = ['Less than 1/10','1 - 3/10', '4 - 6/10', '7 - 8/10', '9 - 9+/10', '10/10', 'Undefined']
    
    iceMap = mapDataFrame.explore(
        column="Concentration", # color by concentration column
        tooltip="Concentration", # show "concentration" value in tooltip (on hover)
        popup=True, # show all values in popup (on click)
        tiles="CartoDB positron", # use "CartoDB positron" tiles
        cmap=cisColorMap, # use custom colormap
        categories=concentrationCategories, # custom categories
        style_kwds=dict(color="black") # use black outline
    )

    # save map as html and load it back in
    short_url = "ctmed_"+mapDateString+".html"
    url = "./data/tmp_maps/ctmed/"+short_url
    iceMap.save(url)

    return short_url

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

def preprocessMapShapefile(mapDataFrame):
    """Perform some preprocessing on the map shapefile. Bucket each variable into the appropriate categories and remove the land and 'X' polygons for the display.

    Args:
        mapDataFrame (geopandas): A geopandas dataframe representation of a CIS combined ice climatology shapefile.

    Returns:
        geopandas: A geopandas dataframe representation of a CIS combined ice climatology shapefile with additional columns.
    """
    # bucket concentrations
    result = []
    for value in mapDataFrame["cpmed"]:
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
    mapDataFrame["cpmed_proc"] = result

    result = []
    for value in mapDataFrame["ctmed"]:
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
    mapDataFrame["ctmed_proc"] = result  

    # bucket predominant ice types
    result = []
    for value in mapDataFrame["pimed"]:
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
    mapDataFrame["pimed_proc"] = result

    result = []
    for value in mapDataFrame["prmed"]:
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
    mapDataFrame["prmed_proc"] = result  

    # ice frequency
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
    mapDataFrame["icfrq_proc"] = result

    # remove land and X from the polygons
    mapDataFrame.query("ctmed != 'L'",inplace=True)
    mapDataFrame.query("ctmed != 'X'",inplace=True)

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
    
    iceMap = mapDataFrame.explore(
        column=mapDisplayVariable+"_proc", # color by concentration column
        tooltip=mapDisplayVariable+"_proc", # show "concentration" value in tooltip (on hover)
        popup=['ctmed_proc','cpmed_proc','icfrq_proc','pimed_proc','prmed_proc'], # show these values in popup (on click)
        tiles="CartoDB positron", # use "CartoDB positron" tiles
        cmap=displayColorMap, # use custom colormap
        categories=displayCategories, # custom categories
        style_kwds=dict(weight=1,opacity=0.3,fillOpacity=0.75) # use thin outline
    )

    # save map as html and load it back in
    short_url = mapDisplayVariable+"_"+mapDateString+".html"
    url = "./data/tmp_maps/combined/"+short_url
    iceMap.save(url)

    return short_url

def createMap(mapFilePath,mapDateString,mapVariable):
    """Generate an interactive HTML map for a given ice climatology variable CIS shapefile.

    Args:
        mapFilePath (str): Relative filepath to the CIS shapefile.
        mapDateString (str): Four character string indicating the month and week of the shapefile data (e.g. '0108').
        mapVariable (str): One of 'ctmed', 'cpmed', 'icfrq', 'pimed', or 'prmed'

    Returns:
        str: The name of the generated html map file.
    """
    return createCombinedIceMap(mapFilePath, mapDateString, mapVariable)