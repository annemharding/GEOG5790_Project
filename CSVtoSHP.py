# -*- coding: utf-8 -*-
"""
GEOG5790 - Programming for Geographical Information Analysis: Advanced Skills
Independent Project - EA WIMS Water Quality Data Analyser/Viewer

Anne Harding (200754573)
02/05/2019

CSVtoSHP.py

ArcGIS Script tool to use water quality .csv files to generate .shp file
containing all EA water quality sampling points across England.
"""

# Import modules:
import arcpy
import os
import glob
import csv
# from timeit import default_timer as timer
import pandas as pd

# -----------------------------------------------------------------------------
# PARAMETERS:

# Read in parameter values from toolbox GUI:
# 0: INPUT - Directory containing .csv files.
# 1: INPUT - Directory to contain .shp files.

csvDir = arcpy.GetParameterAsText(0)
shpDir = arcpy.GetParameterAsText(1)

# -----------------------------------------------------------------------------
# FIND .CSV FILES TO CONVERT:

# Change directory to .csv folder:
os.chdir(csvDir)
# Define extension to search for:
extension = ".csv"

# Use pattern-matching to identify .csv files for EA area:
arcpy.AddMessage("Finding all .csv files to convert to .shp.")
all_filenames = [i for i in glob.glob('*{}'.format(extension))]
# Print statement to manually check number of identified files:
arcpy.AddMessage("{0} .csv files found in {1}:".format(str(len(all_filenames)), csvDir))
for filename in all_filenames:
    arcpy.AddMessage("  - {0}".format(filename))
# -----------------------------------------------------------------------------
# ARC ENVIRONMENTS:

# Set workspace:
arcpy.env.workspace = shpDir
# Set spatial reference to British National Grid (27700):
spRef = arcpy.SpatialReference(27700)
# Allow overwriting of output files:
arcpy.env.overwriteOutput = True

# -----------------------------------------------------------------------------

# Loop through EA operational areas:
for filename in all_filenames:
    
    # Inform user of progress through files:
    arcpy.AddMessage("Processing {0}:".format(filename))
    
    # Get full filepath for .csv:
    area_csv = os.path.join(csvDir, filename)
    
    # Get basename from .csv filepath and strip extension:
    basename = os.path.basename(area_csv).rstrip(os.path.splitext(area_csv)[1])
    
    # Create valid file name for ArcMap by converting hyphens in basename to underscores:
    basename = basename.replace("-","_")
    
    # Print statement to manually check basename:
    # arcpy.AddMessage("basename: {0}".format(basename))
    
    # Define filepaths for scratch output files:
    area_shp_name = basename + ".shp"
    area_shp = shpDir + '\\' + area_shp_name
    
    # Define filepaths for retained output files:
    area_locs = shpDir + '\\' + basename + '_locs.shp'
    monitoring_locs = shpDir + '\\' + "england_wq_locs.shp"
    
    # Print statements to manually check area_shp_name variable and its type:
    # arcpy.AddMessage("area_shp_name: {0}".format(area_shp_name))
    # arcpy.AddMessage("area_shp_name variable type: {0}".format(type(area_shp_name)))
    
    # -------------------------------------------------------------------------
    # CREATE NEW SHAPEFILE AND ADD FIELDS:
    
    arcpy.AddMessage("  - Creating empty shapefile.")
    # Create empty shapefile:
    # Create Feature Class: http://desktop.arcgis.com/en/arcmap/10.3/tools/data-management-toolbox/create-feature-class.htm
    # CreateFeatureclass_management (out_path, out_name, {geometry_type}, {template}, {has_m}, {has_z}, {spatial_reference}, {config_keyword}, {spatial_grid_1}, {spatial_grid_2}, {spatial_grid_3})
    
    # Check if file already exists:
    if os.path.isfile(area_shp):
        # Delete shapefile (and auxilliary files:
        arcpy.Delete_management(area_shp)
        
    arcpy.CreateFeatureclass_management(shpDir, area_shp_name, "POINT", spatial_reference=spRef)
    
    arcpy.AddMessage("  - Adding fields.")
    # Add fields to newly-created shapefile:
    # Add Field: https://pro.arcgis.com/en/pro-app/tool-reference/data-management/add-field.htm
    # AddField_management (in_table, field_name, field_type, {field_precision}, {field_scale}, {field_length}, {field_alias}, {field_is_nullable}, {field_is_required}, {field_domain})
    arcpy.AddField_management(area_shp, "easting", "LONG", 6)
    arcpy.AddField_management(area_shp, "northing", "LONG", 6)
    arcpy.AddField_management(area_shp, "notation", "TEXT")
    arcpy.AddField_management(area_shp, "label", "TEXT")
    
    '''
    # Original attempt at streamlining the code to add fields to the .shp:
    
    fields = [
            ("easting", "LONG"),
            ("northing", "LONG"),
            ("notation", "TEXT"),
            ("label", "TEXT")
            ]
    
    for field in fields:
        arcpy.AddField_management(area_shp, field)
        
    # This code raised the following error:
    # RuntimeError: Object: Error in executing tool
    # which I could not solve, so I opted to repeat the same function 4 times
    # to add each of the fields. Although the original loop would probably
    # have been quicker and looks neater for a human to read.
    '''
    
    # -------------------------------------------------------------------------
    # WRITING .CSV FILE TO .SHP FILE:
    
    arcpy.AddMessage("  - Writing .csv file to .shp file.")
    
    # Specify columns to read in order to avoid encountering a memory error
    # when using large datasets (i.e. .csv files > 2GB):
    use_cols = ["sample.samplingPoint.easting",
               "sample.samplingPoint.northing",
               "sample.samplingPoint.notation",
               "sample.samplingPoint.label"]
    
    # Read .csv file into pandas dataframe:
    df = pd.read_csv(area_csv, usecols = use_cols)
    # Print statement to manually check length of original df:
    # arcpy.AddMessage(df.count())
    
    # Remove duplicate spatial locations from pandas dataframe:
    df = df.drop_duplicates(['sample.samplingPoint.easting', 'sample.samplingPoint.northing'], keep='first')
    # Print statement to manually check length of df with duplicates removed:
    # arcpy.AddMessage(df.count())
    
    # Cursor to insert rows into area_shp:
    cursor = arcpy.InsertCursor(area_shp)
    
    # Timer to check speed of code during testing process:
    #start = timer()
    
    # Loop through rows of pandas dataframe:
    for i, row in df.iterrows():
        
        # Print statement to manually check iteration through rows:
        # arcpy.AddMessage(row)
        
        # Create new feature:
        feature = cursor.newRow()
        vertex = arcpy.CreateObject("Point")
        # Define spatial location:
        vertex.X = row['sample.samplingPoint.easting']      # x coordinate
        vertex.Y = row['sample.samplingPoint.northing']     # y coordinate
        feature.shape = vertex
        
        # Add attributes to feature:
        feature.easting = row["sample.samplingPoint.easting"]   # easting
        feature.northing = row["sample.samplingPoint.northing"] # northing
        feature.notation = row["sample.samplingPoint.notation"] # notation
        feature.label = row["sample.samplingPoint.label"]       # label
        
        # Write feature to .shp:
        cursor.insertRow(feature)
    
    # Timer to check speed of code during testing process:
    # end = timer()
    # arcpy.AddMessage("Time to write .shp: {} seconds.".format((end-start)))
    
    # Delete cursor object:
    del cursor

    # Next .csv to convert...
    
# -----------------------------------------------------------------------------
# COMBINE .SHP FILES:

arcpy.AddMessage("Combining .shp files.")

# Find feature classes in workspace:
fcs = arcpy.ListFeatureClasses()

# Combine all .shp files into one:
# Merge: https://pro.arcgis.com/en/pro-app/tool-reference/data-management/merge.htm
# Merge_management (inputs, output, {field_mappings})
arcpy.Merge_management(fcs, monitoring_locs)
    
'''
Alternative method to convert .csv to .shp:
    
1) 
Make XY Event Layer: http://desktop.arcgis.com/en/arcmap/10.3/tools/data-management-toolbox/make-xy-event-layer.htm
MakeXYEventLayer_management (table, in_x_field, in_y_field, out_layer, {spatial_reference}, {in_z_field})
arcpy.AddMessage("Step 1) Creating xy events from .csv file.")

2)
Save XY Event Layer to .lyr file:
Save To Layer File: https://pro.arcgis.com/en/pro-app/tool-reference/data-management/save-to-layer-file.htm
SaveToLayerFile_management (in_layer, out_layer, {is_relative_path}, {version})

3)
Copy features from .lyr to .shp:
Copy Features: http://desktop.arcgis.com/en/arcmap/10.3/tools/data-management-toolbox/copy-features.htm
CopyFeatures_management (in_features, out_feature_class, {config_keyword}, {spatial_grid_1}, {spatial_grid_2}, {spatial_grid_3})

4)    
Remove duplicate points from .shp:
Dissolve: http://desktop.arcgis.com/en/arcmap/latest/tools/data-management-toolbox/dissolve.htm
Dissolve_management (in_features, out_feature_class, {dissolve_field}, {statistics_fields}, {multi_part}, {unsplit_lines})

'''