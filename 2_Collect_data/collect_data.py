# -*- coding: utf-8 -*-

% cd ~/Master_Data_Science/TFM/2_Collect_data/
% pwd

# This script use sys, re, request, PyQt4, bs4 and pandas python libraries.

import sys
import re
import requests
from bs4 import BeautifulSoup
from PyQt4.QtGui import QApplication
from PyQt4.QtCore import QUrl
from PyQt4.QtWebKit import QWebPage
import pandas as pd

# Collect codes of public elementary schools in municipality of Madrid.

# Url to perform advanced searches.
url_advsearch = "http://www.madrid.org/wpad_pub/run/j/BusquedaAvanzada.icm"

# Parameter for searching public primary schools in municipality of Madrid
params = {"titularidadPublica": "S", "cdMuni": "079", "cdNivelEdu": "6545"}

# Request and parse list of schools.
schools = BeautifulSoup(requests.post(url_advsearch, data = params).content, "lxml")

# Extract list of school codes.
school_codes = schools.findAll(
    attrs = {"name": "codCentrosExp", 
    "value":re.compile("^.+$")})[0]["value"]

# Convert from string to list.
school_codes = school_codes.split(";")

# Check codes.
# 247 it's ok.
# print len(school_codes)


# Let's save the list of school codes in order to use it in this test phase

import pickle

# to save
with open("school_codes.txt", "wb") as f:
    pickle.dump(school_codes, f)


# to open
with open("school_codes.txt", "rb") as f:
    school_codes = pickle.load(f)


<-------------->

# Extract tables from school cards.

# The data that we want to obtain from each school is contained in tables,
# whose content is generated on-the-fly through JavaScript code.
# We can't use 'request' library again because only fetch source code of
# the web page but it doesn't run code. So we need to mimic the rendering
# process of a browser.
# The QtWebKit module, in PyQt4 toolkit library, implements a web browser
# engine based on the WebKit open source browser engine. 


# Create the class 'mimic-render' that is inheriting from QWebPage.
class mimic_render(QWebPage):
	
	def __init__(self, url):
    	self.app = QApplication(sys.argv)
    	QWebPage.__init__(self)
    	self.loadFinished.connect(self.on_page_load)
    	self.mainFrame().load(QUrl(url))
    	self.app.exec_()

	def on_page_load(self, result):
	    self.frame = self.mainFrame()
	    self.app.quit()

# School card url.
url_schoolcard = "http://www.madrid.org/wpad_pub/run/j/MostrarFichaCentro.icm"

# School code parameter.
school_code_par = "cdCentro="

# Url to instance the class 'mimic_render'.
url_card = url_schoolcard+"?"+school_code_par+school_codes[200]

# Create an instance of the class 'mimic_render'.
# QtP4 load the web page creating a 'mimic_render' object, that is
# basically a QWebPage object.
render_content = mimic_render(url_card)

# QtP4 grab the source code from QWebPage.
source = render_content.frame.toHtml()

# Convert QString to string so it can be handled by BeautifulSoup.
formatted_source = str(source.toAscii())

# Parse school card.
school_card = BeautifulSoup(formatted_source, "lxml")

# Extract tables html
school_tables = school_card.findAll('table', class_="tablaGraficaDatos")

# Extract school name
school_name = school_card.find(style="text-transform:uppercase").next.next

print school_name


# Save tables in a dictionary
dataframe_collection = {}

for i, table in list(enumerate(school_tables)):
    if i <= 1:
        dataframe_collection[school_name + "_" + str(i)] = \
        pd.read_html(table.prettify())

print dataframe_collection


# Test with 5 urls.

schools_urls = [url_schoolcard + "?" + school_code_par + code for code in school_codes]

dataframe_collection = {}

for school in schools_urls[:5]:
    render_content = mimic_render(school)
    source = render_content.frame.toHtml()
    formatted_source = str(source.toAscii())
    school_card = BeautifulSoup(formatted_source, "lxml")
    school_tables = school_card.findAll('table', class_="tablaGraficaDatos")
    school_name = school_card.find(style="text-transform:uppercase").next.next
    for i, table in list(enumerate(school_tables)):
        if i <= 1:
            dataframe_collection[school_name + "_" + str(i)] = \
            pd.read_html(table.prettify())

# NOT WORK!!!! WHYYYYYY!!!


# Apparently, only one QApplication can be created in the program.

# Let's try dryscrape

import dryscrape

render = dryscrape.Session()
render.visit("http://www.madrid.org/wpad_pub/run/j/MostrarFichaCentro.icm?cdCentro=28063799")
source = render.body()
school_card = BeautifulSoup(source, "lxml")
school_tables = school_card.findAll('table', class_="tablaGraficaDatos")
school_name = school_card.find(style="text-transform:uppercase").next.next

dataframe_collection = {}

for i, table in list(enumerate(school_tables)):
    if i <= 1:
        dataframe_collection[school_name + "_" + str(i)] = \
        pd.read_html(table.prettify())

type(school_tables)


# It's ok. Let's test it with 5 urls.

url_schoolcard = "http://www.madrid.org/wpad_pub/run/j/MostrarFichaCentro.icm"
school_code_par = "cdCentro="
schools_urls = [url_schoolcard + "?" + school_code_par + code for code in school_codes]

school_tables_collection = {}
school_name_collection = []

render = dryscrape.Session()
for z, school in enumerate(schools_urls[:5]):
    render.visit(school)
    source = render.body()
    school_card = BeautifulSoup(source, "lxml")
    school_tables = school_card.findAll('table', class_="tablaGraficaDatos")
    school_name = school_card.find(style="text-transform:uppercase").next.next
    for i, table in list(enumerate(school_tables)):
        if i <= 1:
            school_tables_collection[school_name + "_" + str(i)] = \
            pd.read_html(table.prettify())
            school_name_collection.append(school_name)
    print "Tables of school %s extracted" % schools_urls[z]

print dataframe_collection

# Perfect!!

# Two tables are being collected: evolution of the number of students and
# evolution of the ratio of students admitted to applications submitted.
# The second table is not correct, because, by default, the page loads the
# data referred to "Infantil". A "click" event must be performed
# on the radio button corresponding to "Primaria".

render = dryscrape.Session()
render.visit("http://www.madrid.org/wpad_pub/run/j/MostrarFichaCentro.icm?cdCentro=28063799")
radiob = render.at_css('#nivEd12\.grafica3')
radiob.click()
source = render.body()
school_card = BeautifulSoup(source, "lxml")
school_tables = school_card.findAll('table', class_="tablaGraficaDatos")
table = list(school_tables)[1]
pd.read_html(table.prettify())


# An error is displayed because one of the parent nodes is not displayed
# (<div id="solapaspanel1" style="display: none;">, and the radio button
# is invisible to the code. 

# Let's try with a little piece of javascript.

render = dryscrape.Session()
render.visit("http://www.madrid.org/wpad_pub/run/j/MostrarFichaCentro.icm?cdCentro=28063799")
render.driver.exec_script('document.getElementById("nivEd12.grafica3").click();')
source = render.body()
school_card = BeautifulSoup(source, "lxml")
school_tables = school_card.findAll('table', class_="tablaGraficaDatos")
table = list(school_tables)[1]
pd.read_html(table.prettify())

# Now it's working. Let's test 5 urls.

school_tables_collection = {}
school_name_collection = []

render = dryscrape.Session()
for z, school in enumerate(schools_urls[:5]):\
    render = dryscrape.Session()
    render.set_attribute('auto_load_images', False)
    render.set_timeout(30)
    render.visit(school)
    render.driver.exec_script('document.getElementById("nivEd12.grafica3").click();')
    time.sleep(1)
    source = render.body()
    school_card = BeautifulSoup(source, "lxml")
    school_tables = school_card.findAll('table', class_="tablaGraficaDatos")
    school_name = school_card.find(style="text-transform:uppercase").next.next
    for i, table in list(enumerate(school_tables)):
        if i <= 1:
            school_tables_collection[school_name + "_" + str(i)] = \
            pd.read_html(table.prettify())
            school_name_collection.append(school_name)
    print "Tables of school %s extracted" % schools_urls[z]
    render.reset()


import time






# de cara a matchear la bbdd del ayuntamiento y la de la comunidad hay que formatear:
# bbdd del ayuntamiento
# - convertir a mayúsculas
# - quitar el string "Colegio Público"
# - quitar acentos y diéresis
#
# bbdd de la comunidad
# - sustituir guión por espacio en blanco
