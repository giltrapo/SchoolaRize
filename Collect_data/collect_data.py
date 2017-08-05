# -*- coding: utf-8 -*-

# This script use sys, request, PyQt4, bs4 and pandas python libraries.

import sys
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
schools = BeautifulSoup(
    requests.post(url_advsearch, data = params).content, "lxml")

# Extract list of school codes.
school_codes = schools.findAll(
    attrs = {"name": "codCentrosExp", 
    "value":re.compile("^.+$")})[0]["value"]

# Convert from string to list.
school_codes = school_codes.split(";")

# Check codes.
# 247 it's ok.
# print len(school_codes)

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

dataframe_collection = {}

for i, table in list(enumerate(school_tables)):
    if i <= 1:
        dataframe_collection[school_name + "_" + str(i)] = \
        pd.read_html(table.prettify())

print dataframe_collection


schools_urls = [url_schoolcard + "?" + school_code_par + code for code in school_codes]


# Test with 5 urls.

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


# de cara a matchear la bbdd del ayuntamiento y la de la comunidad hay que formatear:
# bbdd del ayuntamiento
# - convertir a mayúsculas
# - quitar el string "Colegio Público"
# - quitar acentos y diéresis
#
# bbdd de la comunidad
# - sustituir guión por espacio en blanco
