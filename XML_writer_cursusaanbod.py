# Import all necessary modules
from lxml import etree # lxml is being used instead of ElementTree because lxml can use CDATA which is necessary for this particular XML file
import pandas as pd
import numpy as np
from datetime import datetime

import xml_general

course_information = xml_general.read_course_information(directory = r"D:\Stack\Geo-ICT\Trainingen\repo\courses-xml",
                                                         filename = "Cursussen database.xlsx")
course_planning = xml_general.read_course_planning(directory = r"D:\Stack\Geo-ICT\Trainingen\repo\courses-xml",
                                                   filename = "Cursussen database.xlsx")

# the dataframe with information needed for the website
geoict_df = xml_general.create_geoict_df(information_df = course_information, planning_df = course_planning)

# write the geoict dataframe to a CSV file for importing at the website
geoict_df.to_csv(r"D:\Stack\Geo-ICT\Trainingen\repo\courses-xml\cursusinformatie.csv",
                 sep = ";", index = False)

# make the xml file for springest



