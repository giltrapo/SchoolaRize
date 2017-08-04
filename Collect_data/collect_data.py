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

# url to perform advanced searches
url_advsearch = "http://www.madrid.org/wpad_pub/run/j/BusquedaAvanzada.icm"

# parameter for searching public primary schools in municipality of Madrid
params = {"titularidadPublica": "S", "cdMuni": "079", "cdNivelEdu": "6545"}

# request and parse list of schools
schools = BeautifulSoup(requests.post(url_advsearch, data = params).content, "lxml")

# extract list of school codes
school_codes = schools.findAll(
    attrs = {"name": "codCentrosExp", "value":re.compile("^.+$")})[0]["value"]

# convert from string to list 
school_codes = school_codes.split(";")

# check codes
# 247 it's ok
# print len(school_codes)

<-------------->

# Extract tables from school cards

# The data that we want to obtain from each school is contained in tables, whose content
# is generated on-the-fly through JavaScript code.
# We can't use 'request' library again because only fetch source code of the web page
# but it doesn't run code. So we need to mimic the rendering process of a browser.
# The QtWebKit module, in PyQt4 toolkit library, implements a web browser engine based on
# the WebKit open source browser engine. 


# 
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
url_schocard = "http://www.madrid.org/wpad_pub/run/j/MostrarFichaCentro.icm"

# School code parameter
school_code_par = "cdCentro="


# 
url = "http://www.madrid.org/wpad_pub/run/j/MostrarFichaCentro.icm?cdCentro=28063799"

# QtP4 load the web page creating a 'mimic_render' object, that is basically a QWebPage.
render_content = mimic_render(url)

# QtP4 grab the source code from QWebPage.
source = render_content.frame.toHtml()

# Format 
formatted_source = str(source.toAscii())

# Now we can use Beautiful Soup to parse, navigate and found objects in the source code.
school_card = BeautifulSoup(formatted_source, "lxml")
school_tables = school_card.findAll('table', class_="tablaGraficaDatos")
table = school_tables[0]
import pandas as pd
table = pd.read_html(table.prettify())[0]
table



# de cara a matchear la bbdd del ayuntamiento y la de la comunidad hay que formatear:
# bbdd del ayuntamiento
# - convertir a mayúsculas
# - quitar el string "Colegio Público"
# - quitar acentos y diéresis
#
# bbdd de la comunidad
# - sustituir guión por espacio en blanco

