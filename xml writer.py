# This file contains all functies that are applicable to the making of the different XML files
# Specific functions can be found in the xml_<website>.py file 

# Import all necessary modules
import pandas as pd # for easy dataformatting and conversions
from datetime import datetime # to make date conversions
import os # to join directories and filenames
from lxml import etree

def read_course_information(directory, filename):
    """
    This function will read the database file and returns the course information of all courses in a pandas dataframe.
    ! Every value will be read as a string
    """
    course_information = pd.read_excel(os.path.join(directory, filename),
                                       sheet_name = 'cursussen',
                                       dtype=str,
                                       usecols = ['CursusID', 'Cursusnaam', 'Omschrijving', 'Prijs',
                                                  'Extra_kosten', 'Omschrijving_extra_kosten', 'Duur', 
                                                  'Duur_eenheid', 'URL', 'PDF_URL'])

    return course_information

def read_course_planning(directory, filename):
    """ 
    This function will read the database file and returns the planning of the courses in a pandas dataframe
    ! Every value will be read as a string

    This function will also transform the date and time columns to the right formats for XML (date = yyyy-mm-dd and time  = HH:MM)
    This format is used for the XML in Springest, Edubookers and Studytube
    """
    course_planning = pd.read_excel(os.path.join(directory, filename),
                                    sheet_name = 'planning',
                                    dtype = str)
    
    # Convert date notation
    date_to_datetime = [datetime.strptime(str(course_planning.Datum[idx]), '%d-%m-%Y') for idx in range(len(course_planning))]
    testdatums.Datum = [date_to_datetime[idx].strftime('%Y-%m-%d') for idx in range(len(date_to_datetime))]

    # Convert time notation
    for tijd in ['Begintijd', 'Eindtijd']:
        string_to_datetime = [datetime.strptime(str(course_planning.loc[idx, tijd]), '%H:%M:%S') for idx in range(len(course_planning))]
        course_planning[tijd] = [string_to_datetime[idx].strftime('%H:%M') for idx in range(len(string_to_datetime))]

    return course_planning

def add_product_information(parent, local_ID, information_type, table):
    """
    This function will create nodes with the course information
    """
    new_product_information = etree.SubElement(parent, information_type) # create the new node
    new_product_information.text = str(table[table.ID == local_ID][information_type].values[0]) # indexing based on the unique course ID number

def add_courseday_information(parent, schedule_information, daynumber, table, startday_index):
    """
    This function will create nodes with the course planning information
    """
    new_schedule_information = etree.SubElement(parent, schedule_information) # create the new node
    new_schedule_information.text = str(table.loc[table.RowID == str(int(startday_index) + daynumber), schedule_information].values[0]) # indexing based on the unique RowID