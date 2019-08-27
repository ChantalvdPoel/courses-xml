# Import all necessary modules
from lxml import etree # lxml is being used instead of ElementTree because lxml can use CDATA which is necessary for this particular XML file
import pandas as pd
import numpy as np
from datetime import datetime

import xml_general
#import xml_springest

course_information = xml_general.read_course_information(directory = r"D:\Stack\Geo-ICT\Trainingen\repo\courses-xml",
                                                         filename = "Cursussen database.xlsx")
course_planning = xml_general.read_course_planning(directory = r"D:\Stack\Geo-ICT\Trainingen\repo\courses-xml",
                                                   filename = "Cursussen database.xlsx")

# the dataframe with information needed for the website
geoict_df = xml_general.create_geoict_df(information_df = course_information, planning_df = course_planning)

from lxml import etree
import os
root = etree.Element('events')

for event in geoict_df.eventid:
    event_node = etree.SubElement(root, 'event')
    for column in ['cursusnaam', 'tekst', 'datum']:
        info_node = etree.SubElement(event_node, column)
        info_node.text = geoict_df.loc[geoict_df.eventid == event, column].values[0]

created_tree = etree.ElementTree(root)
output_directory = r"D:\Stack\Geo-ICT\Trainingen\repo\courses-xml"
output_filename = "geoict.xml"
created_tree.write(open(os.path.join(output_directory, output_filename), 'wb'),
                    pretty_print=True, 
                    encoding = 'utf-8',
                    xml_declaration = True)

#course_information_springest = xml_springest.course_information_format_springest(course_information)
#course_planning_springest = xml_springest.course_planning_format_springest(course_planning)

#xml_springest.create_xml_springest(course_information_df = course_information_springest,
#                                   course_planning_df = course_planning_springest,
#                                   output_directory = "D:\Stack\Geo-ICT\Trainingen",
#                                   output_filename = "output_springest.xml")


