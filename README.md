# GEOG5790_Project

This repository contains the scripts, example data and other relevant files for my Independent Project assignment for GEOG5790. I have chosen to create a series of scripts/tools which someone with very little coding or GIS knowledge could use to extract water quality sampling data from the Environment Agency (EA) Water Quality Archive (WQA) (https://environment.data.gov.uk/water-quality/view/landing) for a user-specified area. The tool will then allow the user to view and analyse the data interactively using a Jupyter Notebook.

See '200754573_GEOG5790_Independent_Project.pdf' file for further information about purpose, development and use of repository.

Scripts:
- CSVDownloader.py - Python script to download all data from EA WQA and format into 1 .csv file for each EA operational region (containing all years of data).
- CSVtoSHP.py - ArcGIS Script tool to create a .shp file containing locations of all EA water quality sampling points in England.
- WQLocsIdentifier.py - ArcGIS Script tool to identify EA water quality sampling points within a user-specified area.
- WQDataExtractor.py - ArcGIS Script tool to extract EA water quality sampling data using identified sampling points.
- DataViewer.ipynb - Jupyter Notebook to allow user to plot, map and analyse data.
- WQToolbox.pyt - ArcGIS toolbox containing Script tools.
