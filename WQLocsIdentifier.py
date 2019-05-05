# -*- coding: utf-8 -*-
"""
GEOG5790 - Programming for Geographical Information Analysis: Advanced Skills
Independent Project - EA WIMS Water Quality Data Analyser/Viewer

Anne Harding (200754573)
04/05/2019

WQLocsIdentifier.py

ArcGIS Script tool to identify EA water quality sampling points within a user-
specified region (identified by input .shp for area of interest). Outputs a
.shp file containing locations of identified sampling points. This output .shp
may then be used as an input parameter in WQDataExtractor to extract the data.

Note that the processes in WQLocsIdentifier.py and WQDataExtractor.py were
intended to be combined in the same script. However, ArcGIS applied a lock to
the 'wqPoints_clip' file which could not be removed without ending the
script in which that file was created. Hence, the processes were split into 2
different ArcGIS Script tools, both of which are still located in the same 
ArcGIS Toolbox ('WQToolbox.tbx').
"""

# Import modules:
import arcpy
import os

# -----------------------------------------------------------------------------
# PARAMETERS:

# Read in parameter values from toolbox GUI:
# 0: INPUT - Water quality monitoring points.
# 1: INPUT - Shapefile for area of interest.
# 2: INPUT - Output folder location. 

wqPoints = arcpy.GetParameterAsText(0)
areaOfInterest = arcpy.GetParameterAsText(1)
outDir = arcpy.GetParameterAsText(2)

# -----------------------------------------------------------------------------
# ARC ENVIRONMENTS:

# Allow overwriting of output files:
arcpy.env.overwriteOutput = True
# Set workspace:
arcpy.env.workspace = outDir

# -----------------------------------------------------------------------------

# Define location of output files:
wqPoints_clip = os.path.join(outDir, "wqPoints_clip.shp")

# Clip wqPoints shapefile using areaOfInterest shapefile:
# Clip:  https://pro.arcgis.com/en/pro-app/tool-reference/analysis/clip.htm
# Clip_analysis (in_features, clip_features, out_feature_class, {cluster_tolerance})
arcpy.Clip_analysis(wqPoints, areaOfInterest, wqPoints_clip)

'''
# ALTERNATIVE METHOD OF SELECTING DATA BY LOCATION AND SAVING AS .SHP:
# USING CLIP TOOL IS FASTER AND MORE EFFICIENT.

# Make Feature Layer:
arcpy.MakeFeatureLayer_management(wqPoints, "wqPoints_lyr")

# Select Layer By Location: http://desktop.arcgis.com/en/arcmap/10.3/tools/data-management-toolbox/select-layer-by-location.htm
# SelectLayerByLocation_management (in_layer, {overlap_type}, {select_features}, {search_distance}, {selection_type}, {invert_spatial_relationship})
arcpy.SelectLayerByLocation_management("wqPoints_lyr", "WITHIN", areaOfInterest)

# Get Count: https://pro.arcgis.com/en/pro-app/tool-reference/data-management/get-count.htm
# GetCount_management (in_rows)
count = int(arcpy.GetCount_management("wqPoints_lyr")[0])
arcpy.AddMessage(count)

# Copy Features: https://pro.arcgis.com/en/pro-app/tool-reference/data-management/copy-features.htm
# CopyFeatures_management (in_features, out_feature_class, {config_keyword}, {spatial_grid_1}, {spatial_grid_2}, {spatial_grid_3})
arcpy.CopyFeatures_management("wqPoints_lyr", wqPoints_clip)
'''