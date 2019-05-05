# -*- coding: utf-8 -*-
"""
GEOG5790 - Programming for Geographical Information Analysis: Advanced Skills
Independent Project - EA WIMS Water Quality Data Analyser/Viewer

Anne Harding (200754573)
26/04/2019

CSVDownloader.py

Standalone Python script to download water quality data from EA WIMS archive 
for years 2000 to current year for all EA operational regions, and concatenate
into 1 combined .csv file per EA operation region containing all years' data.
"""

# Note that there are multiple ways of downloading data from the archive.
# I have experimented with the different methods and decided that downloading
# the "pre-defined" datasets and keeping a master copy is the best way to 
# proceed. These datasets are split by year and operational area.
# The web archive is currently in "Beta" and says that the datasets are
# updated every month. At the time of writing this script, the data had last
# been updated on 20th March 2019.

# Search "CHANGEME" for filepaths that will need altering if used on
# different computer.

# Import modules:
import os
import datetime
import requests
import pandas as pd
import io
import glob
# import csv
# from bs4 import BeautifulSoup

# -----------------------------------------------------------------------------
# FUNCTIONS:

# Define function to check HTTP status response code following request:
def http_status_checker(status):
    '''
    Function to check if a webpage request was successful (code 200).
    
    PARAMETERS:
    - status: HTTP response status code
    
    RETURNS: None
    '''
    # HTTP status response code 200 OK status code indicates that the request has
    # succeeded (https://developer.mozilla.org/en-US/docs/Web/HTTP/Status/200).
    # See https://httpstatuses.com/ for more details on status response codes.
    
    # If status response code of request is not equal to 200:
    if status != 200:
        # Raise ConnectionError and print status code for user:
        raise requests.ConnectionError(
                "Status code {} returned. Status code 200 expected."
                .format(status))
    # If status response code is equal to 200:
    # else:
        # Inform user that request was successful:
        # print("Status code {} returned. Request successful.".format(status))
        
# Define function to create directory at user-specified location:
def create_directory(dirPath):
    '''
    Function to create a directory at a user-specified location if that
    directory does not already exist.
    
    PARAMETERS:
    - dirPath: user-specified location for directory to be created
    
    RETURNS: None
    '''
    # Try to create output directory:
    try:
        os.mkdir(dirPath)
        print("Directory {} created.".format(dirPath))
    # If output directory already exists, raise FileExistsError:
    except FileExistsError:
        print("Directory {} already exists.".format(dirPath))
        pass
            
    '''
    # ALTERNATIVE CODE:
    # If output directory does not already exist:
    if not os.path.exists(dirPath):
        # Create directory:
        os.mkdir(dirPath)
        # Inform user that directory has been created:
        print("Directory {} created.".format(dirPath))
    # If output directory already exists:
    else:
        # Inform user that directory already exists:
        print("Directory {} already exists.".format(dirPath))
    '''
    
# -----------------------------------------------------------------------------
# GET NOTATION FOR ENVIRONMENT AGENCY OPERATIONAL AREAS:
        
# .csv file location containing EA operational areas details:
ea_areas = 'Z:\GEOG5790\project\data\ea-area.csv' # CHANGEME

# Read .csv file containing EA operational areas details into pandas dataframe:
areas_df = pd.read_csv(ea_areas, header=0)
# Only keep 'label' and 'notation' columns:
areas_df = areas_df[['label', 'notation']]
# Print statement to manually check dataframe:
# print(areas_df)

# Convert 'notation' column to list:
areas_list = areas_df['notation'].tolist()
# Remove "Regional" from list:
areas_list.remove('R')
# Print statement to manually check list:
# print(areas_list)

print(type(areas_list))

# -----------------------------------------------------------------------------
# DOWNLOAD DATA FROM EA WIMS ARCHIVE:

# URL for EA WIMS API:
root = "http://environment.data.gov.uk/water-quality"

# Get current year:
now = datetime.datetime.now()
current_year = now.year

# Define location of output directory to save data to using today's date:
output_dir = "Z:\GEOG5790\project\data\csv_downloaded_" + str(datetime.date.today()) # CHANGEME
# Print statement to manually check output directory:
# print(output_dir)
# Call create_directory function to create a directory at output_dir:
create_directory(output_dir)

# Loop through each year from 2000 to current year:
for year in range(2000, current_year+1):
    
    # Inform user of progress through years loop:
    print("Downloading data for year {}:".format(year))
    
    for area_notation in areas_list:
        # Find area label from area notation using dataframe as a "look-up":
        area_labels = areas_df['label'].where(
                areas_df['notation'] == area_notation).tolist()
        area_label = [x for x in area_labels if str(x) != 'nan'][0]
        
        # Inform user of progress through areas loop:
        print(" - {} ({})".format(area_label, area_notation))
    
        # Define filename:
        filename = str(year) + "_" + str(area_notation) + ".csv"
        # Join output directory path to filename:
        file = os.path.join(output_dir, filename)
        # Print statement to manually check file:
        # print(file)
    
        # Check if file already exists (i.e. data has already been
        # downloaded today) to avoid repeatedly downloading the same data:
        if os.path.isfile(file):
            # Inform user:
            print("Data already downloaded. Skipping this dataset.")
        # If file does not already exist, continue download:
        else:
            # Define URL to download data from for this year and this area:
            url = root + "/batch/measurement?area=" + str(area_notation) + "&year=" + str(year)
            # Print statement to manually check url:
            # print(url)
            
            # Request data download from URL:
            response = requests.get(url)
            
            # Return status code of request:
            status = response.status_code
            # Call http_status_checker function to confirm successful request:
            http_status_checker(status)
        
            # Return content of request:
            content = response.text
            # Print statement to manually check content of request from url:
            # print(content)
            
            # Read content of rquest into pandas dataframe using io:
            df = pd.read_csv(io.StringIO(content))
            # Write pandas dataframe to .csv file:
            df.to_csv(file)
        
            '''
            # ALTERNATIVE METHOD OF WRITING REQUEST TO CSV:
            
            # This code left artefacts in the final .csv files which meant
            # that some of the data did not line up in the relevant columns,
            # making it very difficult to process in further stages.
            
            # Parse content of request using BeautifulSoup:
            soup = BeautifulSoup(content, 'html.parser')
            
            # Create empty array to hold data:
            data = []
            # Loop through rows in parsed data:
            for row in soup:
                # Append each row to data array:
                data.append([row])
                # Print statement to manually check each row:
                # print(row)
            # Print statement to manually check data:
            # print(data)
            
            # Write data to .csv file:
            with open(file, 'w', newline='') as f:
                writer = csv.writer(f, delimiter=',')
                for row in data:
                    writer.writerow(row)
            '''
            
            # Repeat for next area in loop.
            
    # Repeat for next year in loop.
    
print("Data for years 2000 to {} downloaded for all EA areas.".format(current_year))

# -----------------------------------------------------------------------------
# COMBINE DOWNLOADED .CSV FILES:

# Change directory to working directory:
os.chdir(output_dir)
# Define file extension to search for:
extension = ".csv"

# Define subfolder to save combined .csv files for each EA area:
areas_dir = os.path.join(output_dir, "areas")
# Call create_directory function to create a directory at areas_dir:
create_directory(areas_dir)

# loop through EA operational areas:
for area_notation in areas_list:
    # Find area label from area notation using dataframe as a "look-up":
    area_labels = areas_df['label'].where(
        areas_df['notation'] == area_notation).tolist()
    area_label = [x for x in area_labels if str(x) != 'nan'][0]
    
    # Inform user of progress through areas loop:
    print("Combining files for {} ({}).".format(area_label, area_notation))

    # Use pattern-matching to identify .csv files for EA area:
    print("Finding all .csv files to combine.")
    all_filenames = [i for i in glob.glob('*{}'.format(area_notation + extension))]
    # Print statement to manually check number of identified files:
    print("{} .csv files found: ".format(str(len(all_filenames))))
    # Print statement to manually check names of identified files:
    for filename in all_filenames:
        print(filename)

    # Concatenate all identified files into pandas dataframe::
    print("Concatenating .csv files for {} ({}).".format(area_label, area_notation))
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames], sort=True)
    
    # Define output filename for combined .csv file:
    output_filename = areas_dir + "\alldata_" + area_notation + ".csv"

    # Write pandas dataframe for area to output .csv file::
    print("Writing output .csv file to {}.".format(output_filename))
    combined_csv.to_csv(output_filename, index=False, encoding='utf-8')

print("Data concatenation complete.")

'''
# CODE TO COMBINE ALL DATASETS INTO ONE .CSV FOR ALL REGIONS AND ALL YEARS:
# This code was very slow to run due to the large quantity of files and the 
# significant volume of data within each file. Therefore, I had to compromise
# and create master datasets for each individual EA operational area (for all
# years), rather than a complete dataset for all of England.

# Change directory to working directory:
os.chdir(output_dir)
# Define file extension to search for:
extension = ".csv"
# Define filename to save combined output file to:
output_filename = os.path.join(output_dir, "alldata.csv")

# Use pattern-matching to identify all files with '.csv' extension in directory:
print("Finding all .csv files to combine.")
all_filenames = [i for i in glob.glob('*{}'.format(extension))]
# Print statement to manually check number of identified files:
print("{} .csv files found: ".format(str(len(all_filenames))))
# Print statement to manually check names of identified files:
for filename in all_filenames:
    print(filename)

# Concatenate all identified files:
print("Concatenating .csv files.")
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames], sort=True)

# Write pandas dataframe to output .csv file::
print("Writing output .csv file to {}.".format(filename))
combined_csv.to_csv(output_filename, index=False, encoding='utf-8')
'''
# -----------------------------------------------------------------------------