# Schoolarize

This repository contains the KSchool Data Science Master Project.

The project aims to serve as support to those parents who want to school their children in public schools in the city of Madrid.

To do this, an interactive map has been created in which the following information can be obtained at the **school** level:
- Geographic location.
- Percentage of admissions for the 2016-2017 academic year.
- Forecast of the admissions percentage for the 2017-2018 academic year.

The following data is also available at the **district** level:
- Number of schools.
- Number of places of Primary.
- Population between 6 and 11 years old (primary target of Primary courses).
- Relationship between population from 6 to 11 years old and Primary places.

![Schoolarize screenshot](/images/Schoolarize_screenshot.png)

This repository shows all the code used to carry out the project, so that anyone can replicate it if they wish. Most of the project has been done in Python notebooks, and only a small part was carried out with R.

The structure of the folders contained in the repository reflects the phases followed throughout the project.

## Origin and motivation
You can find a early approach of the project [here](http://htmlpreview.github.io/?https://github.com/giltrapo/SchoolaRize/blob/master/1_TFM_first_approach/TFM_first_approach.html#/).

## Obtaining data
The data used were obtained from the websites of the Community and the City Council of Madrid. The data of the City Council were downloaded directly, in different formats (.csv, .shp, etc.), but those of the Community were obtained running a script to scrape the data of interest. These data were contained in tables, whose content was generated on-the-fly through JavaScript code, so it was necessary to render these tables without having to access them from a browser, by mean of some Python packages.
    
The script can be run directly from the [collect_data.py file](https://github.com/giltrapo/SchoolaRize/blob/master/2_Data_Collect/collect_data.py) or from [collect_data.ipynb notebook](https://github.com/giltrapo/SchoolaRize/blob/master/2_Data_Collect/collect_data.ipynb), contained in the [2_Data_Collect folder](https://github.com/giltrapo/SchoolaRize/tree/master/2_Data_Collect), making sure you have the necessary packages installed first.

## Cleaning and Formatting of Data
The data obtained was modified to adapt it to the subsequent phases of the project. The code for this phase can be found in [data_munging.ipynb notebook](https://github.com/giltrapo/SchoolaRize/blob/master/3_Data_Munging/data_munging.ipynb), contained in the [3_Data_Munging folder](https://github.com/giltrapo/SchoolaRize/tree/master/3_Data_Munging).

## Data Analysis
A small forecast exercise was carried out in which several models were tested to predict the admissions percentage of the 2017-2018 academic year. This phase was done with R, since I am more familiar with this tool when it comes to building mixed models, with fixed and random effects. You can see the analysis process in the [Analysis_phase.md file](https://github.com/giltrapo/SchoolaRize/blob/master/4_Data_Analysis/Analysis_Phase.md), contained in the [4_Data_Analysis folder](https://github.com/giltrapo/SchoolaRize/tree/master/4_Data_Analysis).

## Data Visualization
Finally, a GeoJSON file was created with the data to be displayed, including the geometries of the districts of Madrid, obtained from a shapefile downloaded from the website of the Madrid City Council, and an interactive map was designed with Plotly and Dash. The code for the download and creation of the GeoJSON file is in the [Geofiles_munging.ipynb notebook](https://github.com/giltrapo/SchoolaRize/blob/master/5_Data_Visualization/Geofiles_munging.ipynb). The map can be accessed, for now, by executing the code in [Mapping.ipynb notebook](https://github.com/giltrapo/SchoolaRize/blob/master/5_Data_Visualization/Mapping.ipynb). These files can be located in the [5_Data_Visualization folder](https://github.com/giltrapo/SchoolaRize/tree/master/5_Data_Visualization).
