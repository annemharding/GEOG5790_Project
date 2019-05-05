# GEOG5790_Project

This repository contains the scripts, example data and other relevant files for my Independent Project assignment for GEOG5790. I have chosen to create a series of scripts/tools which someone with very little coding or GIS knowledge could use to extract water quality sampling data from the [Environment Agency (EA) Water Quality Archive (WQA)](https://environment.data.gov.uk/water-quality/view/landing) for a user-specified area. The tool will then allow the user to view and analyse the data interactively using a Jupyter Notebook.

See '200754573_GEOG5790_Independent_Project.pdf' file for further information about purpose, development and use of repository.

This code was developed using University of Leeds computer GEO-GISB-14 (Processor: Intel(R) Core(TM) i7-4790 CPU @ 3.60GHz, Memory: 16.0 GB), ArcMap 10.6 and Python 3.7.3.

The code is structured as follows:
![alt text](https://github.com/annemharding/GEOG5790_Project/blob/master/code_structure.png)

**Scripts**:
- CSVDownloader.py - Python script to download all data from EA WQA and format into 1 .csv file for each EA operational region (containing all years of data).
- CSVtoSHP.py - ArcGIS Script tool to create a .shp file containing locations of all EA water quality sampling points in England.
- WQLocsIdentifier.py - ArcGIS Script tool to identify EA water quality sampling points within a user-specified area.
- WQDataExtractor.py - ArcGIS Script tool to extract EA water quality sampling data using identified sampling points.
- DataViewer.ipynb - Jupyter Notebook to allow user to plot, map and analyse data.
- WQToolbox.tbx - ArcGIS toolbox containing Script tools.

Note that the DataViewer.ipynb Jupyter Notebook must be opened in **Google Chrome** in order to load the widgets properly in the browser. Google Chrome may be downloaded from [here.](https://www.google.co.uk/chrome/?brand=CHBD&gclid=EAIaIQobChMIl-K8u8SE4gIVS7TtCh0OLQM6EAAYASAAEgLypvD_BwE&gclsrc=aw.ds)

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


