# -*- coding: utf-8 -*-
"""
GEOG5790 - Programming for Geographical Information Analysis: Advanced Skills
Independent Project - EA WIMS Water Quality Data Analyser/Viewer

Anne Harding (200754573)
26/04/2019

WQDataExtractor.py

Script to extract data from downloaded water quality archive for user-specified
EA water sampling points (as output from 'WQLocsIdentifier.py'). The user may
also choose here to extract the data for a certain time period only.

Note that the processes in WQLocsIdentifier.py and WQDataExtractor.py were
intended to be combined in the same script. However, ArcGIS applied a lock to
the 'wqPoints_clip' file which could not be removed without ending the
script in which that file was created. Hence, the processes were split into 2
different ArcGIS Script tools, both of which are still located in the same 
ArcGIS Toolbox ('WQToolbox.tbx').
"""

# Import modules:
import arcpy
import arcpy.da
import os
import pandas as pd
import numpy as np
import datetime

# -----------------------------------------------------------------------------
# FUNCTIONS:

# Define function to filter water quality data using user-specified filters:
def data_filter(df):
    '''
    Function to filter water quality data using user-specified filters for
    date range and monitoring locations.
    
    PARAMETERS:
    - df: dataframe containing water quality data
    
    RETURNS: None
    '''
    # Filter dataframe to only keep rows where "sample.samplingPoint.notation"
    # attribute matches the notation of one of the selected WQ monitoring locs:
    df = df.loc[df['sample.samplingPoint.notation'].isin(locs)]
    # Filter dataframe to only keep rows within user-selected time period:
    df = df[(df['sample.sampleDateTime'] > startDate) & (df['sample.sampleDateTime'] < endDate)]
    
# -----------------------------------------------------------------------------
# PARAMETERS:

# Read in parameter values from toolbox GUI:
# 0: INPUT - Selected water quality monitoring points.
# 1: INPUT - Water quality data archive.
# 2: INPUT - EA operational area.
# 3: INPUT - Start date (defaults to 01/01/2000).
# 4: INPUT - End date (defaults to current date).
# 5: INPUT - Output folder location.

wqPoints_clip = arcpy.GetParameterAsText(0)
wqArchive = arcpy.GetParameterAsText(1)
eaArea = arcpy.GetParameterAsText(2)
startDate = arcpy.GetParameterAsText(3)
endDate = arcpy.GetParameterAsText(4)
outDir = arcpy.GetParameterAsText(5)

# TODO - Would like to include an option here which allows the user to select
# which determinands they are interested in. For future development.

# Reformat startDate and endDate for comparison with dataframe later on: 
startDate = str(datetime.datetime.strptime(startDate, '%d/%m/%Y'))
endDate = str(datetime.datetime.strptime(endDate, '%d/%m/%Y'))

# Print statement to manually check re-formatting of dates:
# arcpy.AddMessage(startDate)
# arcpy.AddMessage(endDate)

# -----------------------------------------------------------------------------
# ARC ENVIRONMENTS:

# Allow overwriting of output files:
arcpy.env.overwriteOutput = True
# Set workspace:
arcpy.env.workspace = outDir

# -----------------------------------------------------------------------------
# GET LIST OF WQ MONITORING LOCATIONS:

# Create empty locs array to hold list of WQ monitoring locations of interest:
locs = []

arcpy.AddMessage("Identifying WQ monitoring locations selected.")

# Define SearchCursor for .shp containing selected monitoring points:
# Search Cursor: https://pro.arcgis.com/en/pro-app/arcpy/data-access/searchcursor-class.htm
# SearchCursor(in_table, field_names, {where_clause}, {spatial_reference}, {explode_to_points}, {sql_clause})
# Use 'with' statement to prevent relics further down the script.
with arcpy.da.SearchCursor(wqPoints_clip, '*') as cursor:
    # Loop through rows in the cursor:
    for row in cursor:
        # Print statement to manually check return:
        # arcpy.AddMessage(row)
        # Get "notation" attribute for row:
        loc = row[5]
        # Append "notation" attribute for row to locs list:
        locs.append(loc)

arcpy.AddMessage("{0} sites selected:".format(len(locs)))
for loc in locs:
    arcpy.AddMessage("  - {0}".format(loc))
    
# -----------------------------------------------------------------------------
# USE LIST OF WQ MONITORING LOCATIONS TO EXTRACT DATA FROM ARCHIVE:    

# Using index of "(" and ")" in eaArea variable to get notation:
start_loc = eaArea.find("(")
end_loc = eaArea.find(")")
eaArea_notation = eaArea[start_loc+1:end_loc]
# Print statement to manually check eaArea_notation variable:
# arcpy.AddMessage(eaArea_notation)

# Find required .csv file using wqArchive directory and eaArea:
datafile = wqArchive + "\\" + "alldata_" + eaArea_notation + ".csv"

arcpy.AddMessage("Collecting archive data from: {0}.".format(datafile))

# Try to read .csv file:
try:
    # Read wqArchive .csv into a pandas dataframe:
    df = pd.read_csv(datafile, header=0)
    
    arcpy.AddMessage("Filtering data.")
    # Call data_filter function using user-specified filters to extract data:
    df_filtered = data_filter(df)

# Except if memory error is encountered (i.e. file is too large):
except MemoryError:
    # Read .csv file into a pandas dataframe in chunks:
    chunks = pd.read_csv(datafile, sep=',', chunksize=10000)
    
    arcpy.AddMessage("Filtering data.")
    # Filter chunks using list of selected sampling points:
    chunks = [chunk[chunk['sample.samplingPoint.notation'].isin(locs)] for chunk in chunks]
    # Filter chunks using user-specified dates:
    chunks = [chunk[(chunk['sample.sampleDateTime'] > startDate) & (chunk['sample.sampleDateTime'] < endDate)] for chunk in chunks]      
    
    # Concatenate filtered chunks into one pandas dataframe:
    df_filtered = pd.concat(chunks)
    # Print statement to check filtered dataframe:
    # arcpy.AddMessage(df_filtered)
    
arcpy.AddMessage("Processing data for values below Limit of Detection.")
# Standard data pre-processing for values below (<) Limit of Detection (LoD)
# is to halve the value and perform analysis using the halved value:
df_filtered['resultQualified'] = np.where(df_filtered['resultQualifier.notation'] == '<', df_filtered['result']/2, df_filtered['result'])

arcpy.AddMessage("Exporting filtered data to .csv file.")
# Writing pandas dataframe to .csv file:
df_filtered.to_csv(os.path.join(outDir, "selected_data.csv"))