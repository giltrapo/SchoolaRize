#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Collect data script"""

import re
import requests
from bs4 import BeautifulSoup
import pandas as pd
import pickle
import dryscrape
from time import sleep
from random import randint
from sys import stdout

### Collect codes of public elementary schools in municipality of Madrid.

# Url to perform advanced searches.
url_advsearch = "http://www.madrid.org/wpad_pub/run/j/BusquedaAvanzada.icm"
# Parameter for searching public primary schools in municipality of Madrid
params = {"titularidadPublica": "S", "cdMuni": "079", "cdNivelEdu": "6545"}
# Request and parse list of schools.
schools = BeautifulSoup(requests.post(url_advsearch, data = params).content, "lxml")
# Extract list of school codes.
school_codes = schools.findAll(attrs = {"name": "codCentrosExp", "value": re.compile("^.+$")})[0]["value"]
# Convert from string to list.
school_codes = school_codes.split(";")
# Save list of school codes
with open("Files/school_codes", "wb") as f:
    pickle.dump(school_codes, f)

### Extract tables from school cards.

# School card url.
url_schoolcard = "http://www.madrid.org/wpad_pub/run/j/MostrarFichaCentro.icm"
# School code parameter.
school_code_par = "cdCentro="
# List of schools urls.
schools_urls = [url_schoolcard + "?" + school_code_par + code for code in school_codes]
# Collect data.
school_tables_collection = {}
sts = 0
nsts = 0

for z, school in enumerate(schools_urls):
    try:
        render = dryscrape.Session()
        render.visit(school)
        render.exec_script('document.getElementById("nivEd12.grafica3").click();')
        source = render.body()
        school_card = BeautifulSoup(source, "lxml")
        school_tables = school_card.findAll('table', class_="tablaGraficaDatos")
        school_name = school_card.find(style="text-transform:uppercase").next.next
        for i, table in list(enumerate(school_tables)):
            if i <= 1:
                school_tables_collection[school_name + "_" + str(i)] = pd.read_html(table.prettify())
        sts += 1
        get_ipython().system('echo "Tables of school {school_name} ({schools_urls[z]}) extracted" >> Files/scrape_log')
        stdout.write("\rSchools with statistics: %i, Schools without statistics: %i, Total: %i" % (sts, nsts, sts + nsts))
        stdout.flush()
        render.reset()
        sleep(randint(1, 4))
    except:
        source = render.body()
        school_card = BeautifulSoup(source, "lxml")
        school_name = school_card.find(style="text-transform:uppercase").next.next
        school_tables_collection[school_name + "_" + 0] = []
        school_tables_collection[school_name + "_" + 1] = []
        nsts += 1
        get_ipython().system('echo "School {school_name} ({schools_urls[z]}) doesn\'t have statistics" >> Files/scrape_log')
        stdout.write("\rSchools with statistics: %i, Schools without statistics: %i, Total: %i" % (sts, nsts, sts + nsts))
        stdout.flush()
        sleep(randint(1, 4))
stdout.write("\n")

# Save dictionary with tables
with open("Files/school_tables_collection", "wb") as f:
    pickle.dump(school_tables_collection, f, protocol=pickle.HIGHEST_PROTOCOL)
