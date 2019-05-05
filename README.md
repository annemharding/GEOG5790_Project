# GEOG5790_Project

This repository contains the scripts, example data and other relevant files for my Independent Project assignment for GEOG5790. I have chosen to create a series of scripts/tools which someone with very little coding or GIS knowledge could use to extract water quality sampling data from the [Environment Agency (EA) Water Quality Archive (WQA)](https://environment.data.gov.uk/water-quality/view/landing) for a user-specified area. The tool will then allow the user to view and analyse the data interactively using a Jupyter Notebook.

See '200754573_GEOG5790_Independent_Project.pdf' file for further information about purpose, development and use of repository.

This code was developed using University of Leeds computer GEO-GISB-14 (Processor: Intel(R) Core(TM) i7-4790 CPU @ 3.60GHz, Memory: 16.0 GB), ArcMap 10.6 and Python 3.7.3.

The code is structured as follows:
![alt text](https://github.com/annemharding/GEOG5790_Project/blob/master/code_structure.png)
Note that Stage 1 is only intended to be run infrequently (every few months) in order to process any updated data. It is expected that the outputs from Stage 1 will be kept as an "archive". Stage 2 and 3 may be run whenever it is necessary to extract, view and analyse water quality data for an area of interest. Stage 2 relies on the archive from Stage 1.

**Scripts**:

The following 5 scripts are included in this repository:
- [CSVDownloader.py](https://github.com/annemharding/GEOG5790_Project/blob/master/CSVDownloader.py) - Python script to download all data from EA WQA and format into 1 .csv file for each EA operational region (containing all years of data).
- [CSVtoSHP.py](https://github.com/annemharding/GEOG5790_Project/blob/master/CSVtoSHP.py) - ArcGIS Script tool to create a .shp file containing locations of all EA water quality sampling points in England.
- [WQLocsIdentifier.py](https://github.com/annemharding/GEOG5790_Project/blob/master/WQLocsIdentifier.py) - ArcGIS Script tool to identify EA water quality sampling points within a user-specified area.
- [WQDataExtractor.py](https://github.com/annemharding/GEOG5790_Project/blob/master/WQDataExtractor.py) - ArcGIS Script tool to extract EA water quality sampling data using identified sampling points.
- [DataViewer.ipynb](https://github.com/annemharding/GEOG5790_Project/blob/master/DataViewer.ipynb) - Jupyter Notebook to allow user to plot, map and analyse data.

Note that the DataViewer.ipynb Jupyter Notebook must be opened in **Google Chrome** in order to load the widgets properly in the browser. Google Chrome may be downloaded from [here.](https://www.google.co.uk/chrome/?brand=CHBD&gclid=EAIaIQobChMIl-K8u8SE4gIVS7TtCh0OLQM6EAAYASAAEgLypvD_BwE&gclsrc=aw.ds)

**Tools**:

This project makes use of an ArcGIS toolbox to host the 3 ArcGIS Script tools detailed above:
- WQToolbox.tbx - ArcGIS toolbox containing Script tools.

**Data**:

The following data files are provided within the [WQData_Selected.zip file](https://github.com/annemharding/GEOG5790_Project/blob/master/WQData_selected.zip) (63.6 MB compressed; 1.16 GB uncompressed):
- england_wq_locs shapefile: .shp file containing locations of all EA sampling points in England (output from initial Stage 1 data processing).
- ea-areas.csv - .csv file containing details for each of the EA operational areas (required for Stage 1) CSVDownloader.py).
- EA_AdminBound shapefile - .shp file containing boundaries of each EA operational area (for information).
- alldata_3-35.csv - Example water quality data for one of the EA operational areas (example output from Stage 1) CSVDownloader.py) (contained within 'selected_WQ_areas_downloaded_2019_04_27' subdirectory).
- test_data_small - Folder containing outputs from Stages 2 and 3 for smaller example dataset (26 sampling points).
- test_data_large - Folder containing outputs from Stages 2 and 3 for larger example dataset (116 sampling points).

Note that due to restrictions on individual file size and repository size, water quality data from only one of the sixteen EA operational regions has been uploaded (Northumberland Durham and Tees (3-35)). Therefore, it will only be possible to test Stage 2 (WQLocsIdentifier.py and WQDataExtractor.py) by using data contained within this EA operational region. The tool, however, does still work for all areas in England.

**Python Modules Required:** *(listed alphabetically)*
- arcpy
- convertbng
- csv
- datetime
- folium
- glob
- io
- IPython
- ipywidgets
- matplotlib
- numpy
- os
- pandas
- plotly
- requests
- timeit

Happy analysing!
