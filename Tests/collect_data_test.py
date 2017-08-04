# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup

url_form = "http://www.madrid.org/wpad_pub/run/j/MostrarConsultaGeneral.icm"
url_POST = "http://www.madrid.org/wpad_pub/run/j/BusquedaSencilla.icm"
url_POST_adv = "http://www.madrid.org/wpad_pub/run/j/BusquedaAvanzada.icm"

r = requests.get(url_form)
r.url
print(r.text)

for i,line in enumerate(r.iter_lines()):
    print line
    if i >= 10:
        break

# parameter to call in url_POST
#
# basica.strCodNomMuni=[SCHOOL_NAME]

post_call = {"basica.strCodNomMuni": "adolfo suarez"}
r_post = requests.post(url_POST, data=post_call)

for i,line in enumerate(r_post.iter_lines()):
    print line
    if i >= 10:
        break

for i,line in enumerate(r_post.iter_lines()):
    if 535 <= i <= 566:
        print line

# parameters to call in url_POST_adv
#
# Titularidad Pública:
# titularidadPublica=S
#
# Municipio Madrid:
# cdMuni=079
# comboMunicipios=079
#
#
# 1º Ciclo de Educación Infantil:
# cdTramoEdu=0010
# cdNivelEdu=6027
#
#
# 2º Ciclo de Educación Infantil:
# cdTramoEdu=0020
# cdNivelEdu=6032
#
#
# Educación Primaria:
# cdTramoEdu=0030
# cdNivelEdu=6545
#
#
# Educación Secundaria Obligatoria:
# cdTramoEdu=0040
# cdNivelEdu=6883

post_adv_call ={"titularidadPublica": "S", "cdMuni": "079", "cdNivelEdu": "6545"}

r_post_adv = requests.post(url_POST_adv, data=post_adv_call)

for i,line in enumerate(r_post_adv.iter_lines()):
    if i == 3971:
        print line

source = r_post_adv.content

parsource = BeautifulSoup(source, "lxml")

# or
# parsource = BeautifulSoup(requests.post(url_POST_adv, post_adv_call).content, "lxml")

school_codes = parsource.findAll(
    attrs={"name": "codCentrosExp", "value":re.compile("^.+$")})[0]["value"]

school_codes = school_codes.split(";")

school_codes[0]

codeschool = school_codes[0]
post_call ={"cdCentro": school_codes[0]}
r_post = requests.post(url_schoolcard, data=post_call).content
school_card = BeautifulSoup(r_post, "lxml")
print school_card.prettify()

# Extract tables from school cards


url_schocard = "http://www.madrid.org/wpad_pub/run/j/MostrarFichaCentro.icm"
code_school = {"cdCentro": school_codes[200]}
school_card = BeautifulSoup(requests.post(url_schocard, data = code_school).content, "lxml")
school_tables = school_card.findAll('table', class_="tablaGraficaDatos")

print school_tables

# something is wrong! there is no data in the tables
