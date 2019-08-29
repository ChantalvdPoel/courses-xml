# The purpose of this script is to read in the export of the wpgeo cursusdatums table (website database)
# and convert this to the format that is used in the "Cursussen database" excel workbook

import pandas as pd
from datetime import datetime
import re

wpgeo = pd.read_csv(r"D:\Stack\Geo-ICT\Trainingen\repo\courses-xml\wpgeo_cursusdatums_export_2019_08_28.csv", sep = ";")
cursus_info = pd.read_excel(r"D:\Stack\Geo-ICT\Trainingen\repo\courses-xml\Cursussen database.xlsx",
                            sheet_name = 'cursussen',
                            dtype=str,
                            usecols = ['CursusID', 'Cursusnaam', 'Frequentie'])

op_afroep_db = cursus_info.loc[cursus_info.Frequentie == "op afroep", 'Cursusnaam']


maanden = {'januari': 1, 'februari': 2, 'maart': 3, 'april': 4, 'mei': 5, 'juni': 6, 
           'juli': 7, 'augustus': 8, 'september': 9, 'oktober': 10, 'november': 11, 'december': 12}

output = pd.DataFrame(columns = ['CursusID', 'Cursusnaam', 'Locatie', 'Dag', 'Datum', 'tekstje'])

rijnummer = 0

op_afroep = []

for i in range(len(wpgeo.tekst)):

    compleet = wpgeo.tekst[i]

    dagen = re.findall("[\,\s][0-9]{1,2}[\,\s]", compleet)
    dagen = [d.replace(",", "") for d in dagen]

    if len(dagen) == 0:
        op_afroep.append(wpgeo.cursusnaam[i])
    else:
        maand = [m for m in list(maanden.keys()) if m in compleet] # risico op spelfouten!
        maand_getal = [maanden[m] for m in maand]

        locatie = compleet.split("in ")[-1]

        cursusnaam = wpgeo.cursusnaam[i]

        cursusid = cursus_info.loc[cursus_info.Cursusnaam == cursusnaam, 'CursusID'].values[0]

        if len(maand) == 1:
            for dag in range(1, len(dagen)+1):
            
                output.loc[rijnummer, 'CursusID'] = cursusid

                output.loc[rijnummer, 'Cursusnaam'] = cursusnaam

                output.loc[rijnummer, 'Locatie'] = locatie

                output.loc[rijnummer, 'Dag'] = dag

                output.loc[rijnummer, 'Datum'] = datetime(2019, maand_getal[0], int(dagen[dag-1])).strftime("%Y-%m-%d")

                output.loc[rijnummer, 'tekstje'] = compleet # to check

                rijnummer += 1
        else:
            maand1 = compleet.split(maand[0])[0]
            maand2 = compleet.split(maand[0])[1]

            dagen_maand1 = re.findall("[\,\s][0-9]{1,2}[\,\s]", maand1)
            dagen_maand2 = re.findall("[\,\s][0-9]{1,2}[\,\s]", maand2)

            dagen_maand1 = [d.replace(",", "") for d in dagen_maand1]
            dagen_maand2 = [d.replace(",", "") for d in dagen_maand2]

            dagnummer = 1
            for dag in range(1, len(dagen_maand1)+1):

                output.loc[rijnummer, 'CursusID'] = cursusid

                output.loc[rijnummer, 'Cursusnaam'] = cursusnaam

                output.loc[rijnummer, 'Locatie'] = locatie

                output.loc[rijnummer, 'Dag'] = dagnummer

                output.loc[rijnummer, 'Datum'] = datetime(2019, maand_getal[0], int(dagen_maand1[dag-1])).strftime("%Y-%m-%d")

                output.loc[rijnummer, 'tekstje'] = compleet # to check

                rijnummer += 1

                dagnummer += 1

            for dag in range(1, len(dagen_maand2)+1):

                output.loc[rijnummer, 'CursusID'] = cursusid

                output.loc[rijnummer, 'Cursusnaam'] = cursusnaam

                output.loc[rijnummer, 'Locatie'] = locatie

                output.loc[rijnummer, 'Dag'] = dagnummer

                output.loc[rijnummer, 'Datum'] = datetime(2019, maand_getal[1], int(dagen_maand2[dag-1])).strftime("%Y-%m-%d")

                output.loc[rijnummer, 'tekstje'] = compleet # to check

                rijnummer += 1

                dagnummer += 1

        
output.to_excel(r"D:\Stack\Geo-ICT\Trainingen\repo\courses-xml\recente planning.xlsx")        

        

