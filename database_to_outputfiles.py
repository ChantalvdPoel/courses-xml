# Import all necessary modules
from lxml import etree # lxml is being used instead of ElementTree because lxml can use CDATA which is necessary for this particular XML file
import pandas as pd
import numpy as np
from datetime import datetime
import os

import xml_general
import xml_springest

course_information = xml_general.read_course_information(directory = r"D:\Stack\Geo-ICT\Trainingen\repo\courses-xml",
                                                         filename = "Cursussen database.xlsx")
course_planning = xml_general.read_course_planning(directory = r"D:\Stack\Geo-ICT\Trainingen\repo\courses-xml",
                                                   filename = "Cursussen database.xlsx")

def create_cursusdatums_website(information_df, planning_df, output_directory, output_filename):
    """
    This function will create the dataframe that can be uploaded to the geo-ict website for the forms (cursusdatums)
    It will make the dataframe and write it to a csv file that can be uploaded in the PHP environment of the website
    """
    geoict_df = xml_general.create_geoict_df(information_df = information_df, planning_df = planning_df)
    geoict_df.to_csv(os.path.join(output_directory, output_filename), sep = ";", index = False)

create_cursusdatums_website(information_df = course_information, 
                            planning_df = course_planning, 
                            output_directory = r"D:\Stack\Geo-ICT\Trainingen\repo\courses-xml\output",
                            output_filename = "cursusdatums.csv")

course_information_springest = xml_springest.course_information_format_springest(course_information)
course_planning_springest = xml_springest.course_planning_format_springest(course_planning)

xml_springest.create_xml_springest(course_information_df = course_information_springest,
                                   course_planning_df = course_planning_springest,
                                   output_directory = r"D:\Stack\Geo-ICT\Trainingen\repo\courses-xml\output",
                                   output_filename = "output_springest.xml")


