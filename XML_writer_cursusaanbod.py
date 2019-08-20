# Import all necessary modules
from lxml import etree # lxml is being used instead of ElementTree because lxml can use CDATA which is necessary for this particular XML file
import pandas as pd
import numpy as np
from datetime import datetime

import xml_springest
import xml_general

course_information = xml_general.read_course_information(directory = "D:\Stack\Geo-ICT\Trainingen",
                                                         filename = "Cursussen database V7.xlsx")
course_planning = xml_general.read_course_planning(directory = "D:\Stack\Geo-ICT\Trainingen",
                                                   filename = "Cursussen database V7.xlsx")

course_information_springest = xml_springest.course_information_format_springest(course_information)
course_planning_springest = xml_springest.course_planning_format_springest(course_planning)

xml_springest.create_xml_springest(course_information_df = course_information_springest,
                                   course_planning_df = course_planning_springest,
                                   output_directory = "D:\Stack\Geo-ICT\Trainingen",
                                   output_filename = "output_springest.xml")


