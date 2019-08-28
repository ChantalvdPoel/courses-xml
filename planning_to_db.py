# The purpose of this script is to read in the export of the wpgeo cursusdatums table (website database)
# and convert this to the format that is used in the "Cursussen database" excel workbook

import pandas as pd
from datetime import datetime
import re

wpgeo = pd.read_csv(r"D:\Stack\Geo-ICT\Trainingen\repo\courses-xml\wpgeo_cursusdatums_export_2019_08_28.csv", sep = ";")

maanden = {'januari': 1, 'februari': 2, 'maart': 3, 'april': 4, 'mei': 5, 'juni': 6, 
           'juli': 7, 'augustus': 8, 'september': 9, 'oktober': 10, 'november': 11, 'december': 12}

for i in range(len(wpgeo.tekst)):

    compleet = wpgeo.tekst[i]

    dagen = re.search("[0-9]{1,2}[\,\s]", compleet)
    if dagen == None:
        continue #is op afroep als er geen getallen in staan
    else:
        print(dagen.group()[0])

    maand = [m for m in list(maanden.keys()) if m in compleet] # risico op spelfouten!


