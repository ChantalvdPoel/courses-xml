# This file will make the XML file for Springest
from lxml import etree
import pandas as pd
from datetime import datetime
import os

import xml_general

def course_information_format_springest(course_information_df, website):
    """
    This function will transform the course information dateframe to a format that can be used to make the Springest XML
    The function will:
        - change the column names to the names that are used in the nodes
        - add columns with fixed values
        - add columns that need a bit of calculation
        - order the columns in the order of the nodes in the XSD
    """
    # rename the column that will be used in the XML file
    if website == 'springest':
        columnnames = {'CursusID': 'ID', 
                       'Cursusnaam': 'Name', 
                       'Omschrijving': 'Description',
                       'Prijs': 'Price', 
                       'Extra_kosten': 'AdditionalCosts', 
                       'Omschrijving_extra_kosten': 'AdditionalCosts_description',
                       'Duur': 'Duration', 
                       'Duur_eenheid': 'Duration_unit', 
                       'Max_deelnemers': 'MaxParticipants',
                       'URL': 'WebAddress', 
                       'PDF_URL': 'PdfBrochure'}

        fixed_values = pd.DataFrame({'columnname': ['Language', 'VatIncluded', 'PricePeriod', 'PriceComplete',
                                                'CourseType', 'Completion', 'ProductType'],
                                     'value': ['nl', 'no', 'all', 'true', 'course', 'Certificaat', 'open']})


    elif website == 'studytube':
        columnnames = {'CursusID': 'ID',
                       'Cursusnaam': 'Name',
                       'Omschrijving': 'Description',
                       'Prijs': 'TrainingPriceExVAT',
                       'Extra_kosten': 'AdditionalCosts',
                       'Omschrijving_extra_kosten': 'AdditionalCosts_description',
                       'Categorie': 'Category',
                       'Onderwerp': 'SubCategory',
                       'Duur': 'Duration',
                       'URL': 'WebAddress',
                       'PDF_URL': 'PdfBrochure'}

        fixed_values = pd.DataFrame({'columnname': ['Language', 'VATPercentage', 'Certificate', 'TargetEducationalLevel'],
                                     'value': ['nl', '21', 'Certificaat opleider', 'HBO']})


    elif website == 'edubookers':
        columnnames = {'CursusID': 'ID',
                       'Cursusnaam': 'Name',
                       'Omschrijving': 'Description',
                       'Extra_kosten': 'Additional_costs',
                       'Omschrijving_extra_kosten': 'Additional_costs_description',
                       'Max_deelnemers': 'Max_participants'}

        fixed_values = pd.DataFrame({'columnname': ['Type', 'Complete'],
                                     'value': ['open', 'certificaat']})

    else:
        raise ValueError('dit is geen correcte website, kies uit: springest, studytube of edubookers')


    # Change the column names to the names that are used in the nodes (in the XSD)
    course_information_springest = course_information_df.rename(columns = columnnames)

    # add columns with fixed values
    
    for new_column in fixed_values.columnname:
        course_information_springest[new_column] = fixed_values.loc[fixed_values.columnname == new_column, 'value'].values[0]

    # add columns that need a bit of calculation
    course_information_springest['VatAmount'] = course_information_springest.Price.apply(lambda x: str(round((int(x)*0.21),2))) # adds the amount of VAT (BTW)

    for rows in range(len(course_information_springest)): # add the duration unit based on the Dutch value (dagen of weken)
        if course_information_springest.loc[rows, 'Duration_unit'] == 'dagen':
            course_information_springest.loc[rows, 'DurationUnit'] = 'days'
        elif course_information_springest.loc[rows, 'Duration_unit'] == 'weken':
            course_information_springest.loc[rows, 'DurationUnit'] = 'weeks'

    # order the columns in the order of the nodes in the XSD
    course_information_springest = course_information_springest[['ID', 'Name', 'Description', 'Language', 'Price', 
                                                                 'VatIncluded', 'VatAmount', 'PricePeriod', 
                                                                 'AdditionalCosts', 'PriceComplete', 'CourseType', 
                                                                 'Duration', 'DurationUnit', 'Completion', 
                                                                 'MaxParticipants', 'WebAddress', 'PdfBrochure', 'ProductType']]

    return course_information_springest

def course_planning_format_springest(course_planning_df):
    """
    This function will transform the course planning dateframe to a format that can be used to make the Springest XML
    The function will:
        - change the column names to the names that are used in the nodes
    """
    course_planning_springest = course_planning_df.rename(columns = {'CursusID': 'ID',
                                                                     'Locatie': 'Place',
                                                                     'Dag': 'Day',
                                                                     'Datum': 'Date',
                                                                     'Begintijd': 'StartTime',
                                                                     'Eindtijd': 'EndTime'})

    return course_planning_springest

def springest_create_product(parent, local_ID, table, edubookers = False):
    # Will add all the courses to the Products root as new nodes
    # Makes use of the create_basic_information function to provide all the basic information for every course
    for colname in table.columns.tolist(): # for every column in the table with basic information, do this function
        if (table.loc[table.ID == local_ID, colname].values[0] != 0): # only add information if it is available (not 0)
            if edubookers:
                if (colname == 'Name') | (colname == 'Description'): # if it's a name of description, use CDATA instead or a regular string
                    new_product_information = etree.SubElement(parent, 'training_'+colname.lower()) # create the new node
                    new_product_information.text = etree.CDATA(table[table.ID == local_ID][colname].values[0]) # indexing based on the unique course ID number
                elif (colname == 'Additional_costs') | (colname == 'Additional_costs_description'):
                    continue
                elif (colname == 'ID'):
                    new_product_information = etree.SubElement(parent, 'training_'+colname.lower())
                    new_product_information.text = 'COURSE_'+str(table[table.ID == local_ID]['ID'].values[0])
                else:
                    xml_general.add_product_information(parent = parent, 
                                                        local_ID = local_ID, 
                                                        information_type = colname,
                                                        table = table,
                                                        edubookers = edubookers)
            else:
                if (colname == 'Name') | (colname == 'Description'): # if it's a name of description, use CDATA instead or a regular string
                    new_product_information = etree.SubElement(parent, colname) # create the new node
                    new_product_information.text = etree.CDATA(table[table.ID == local_ID][colname].values[0]) # indexing based on the unique course ID number
                elif (colname == 'AdditionalCosts') | (colname == 'AdditionalCosts_description'):
                    continue
                elif (colname == 'ID'):
                    new_product_information = etree.SubElement(parent, colname)
                    new_product_information.text = 'COURSE_'+str(table[table.ID == local_ID]['ID'].values[0])
                else:
                    xml_general.add_product_information(parent = parent, 
                                                        local_ID = local_ID, 
                                                        information_type = colname,
                                                        table = table)

def springest_create_schedules(parent, local_ID, table_info, table_planning, duration, startdays, amount_startdays):
    # Will create the nodes with information about the planning including the schedule with all the coursedays
    for i in range(amount_startdays): # for the amount of startdays, add new Schedules
        new_event_child = etree.SubElement(parent, 'StartingDatePlace') # create a new node for the new event

        new_event_ID = etree.SubElement(new_event_child, 'ID')
        new_event_ID.text = str(table_planning.loc[table_planning.RowID == startdays[i], 'EventID'].values[0])

        new_event_startdate = etree.SubElement(new_event_child, 'Startdate')
        new_event_startdate.text = str(table_planning.loc[table_planning.RowID == startdays[i], 'Date'].values[0])

        new_event_enddate = etree.SubElement(new_event_child, 'Enddate')
        new_event_enddate.text = str(table_planning.loc[table_planning.RowID == str(int(startdays[i]) + int(duration) - 1), 'Date'].values[0])

        new_event_place = etree.SubElement(new_event_child, 'Place')
        new_event_place.text = str(table_planning.loc[table_planning.RowID == startdays[i], 'Place'].values[0])

        new_event_startdateismonth = etree.SubElement(new_event_child, 'StartdateIsMonthOnly')
        new_event_startdateismonth.text = 'false'

        new_event_enddateismonth = etree.SubElement(new_event_child, 'EnddateIsMonthOnly')
        new_event_enddateismonth.text = 'false'

        new_event_startguaranteed = etree.SubElement(new_event_child, 'StartGuaranteed')
        new_event_startguaranteed.text = 'false'

        new_schedule = etree.SubElement(new_event_child, 'Schedule') # create the Schedule node
        for days in range(int(duration)): # for the duration of the course, add new Coursedays
            new_courseday = etree.SubElement(new_schedule, 'Courseday') # create the Courseday node 
            for colname in ['Date', 'Place', 'StartTime', 'EndTime']: # for every column with planning information, add this to the Courseday node
                xml_general.add_courseday_information(parent = new_courseday, 
                                                      schedule_information = colname, 
                                                      daynumber = days,
                                                      table = table_planning,
                                                      startday_index = startdays[i])
            name_courseday = etree.Element('Name')
            name_courseday.text = 'Cursusdag ' + str(days+1)
            new_courseday.insert(3, name_courseday)


def springest_add_additional_costs(parent, local_ID, table):
    # if there are any additional costs, add a new node to include these
    new_additional_costs_type = etree.SubElement(parent, 'Type')
    new_additional_costs_type.text = 'study material'

    new_additional_costs_price = etree.SubElement(parent, 'Price')
    new_additional_costs_price.text = str(table.loc[table.ID == local_ID, 'AdditionalCosts'].values[0])

    new_additional_costs_vatincluded = etree.SubElement(parent, 'VatIncluded')
    new_additional_costs_vatincluded.text = 'no'

    new_additional_costs_vatamount = etree.SubElement(parent, 'VatAmount')
    new_additional_costs_vatamount.text = str(int(table.loc[table.ID == local_ID, 'AdditionalCosts'].values[0])*0.21)

    new_additional_costs_mandatory = etree.SubElement(parent, 'Mandatory')
    new_additional_costs_mandatory.text = 'true'

def create_xml_springest(course_information_df, course_planning_df, output_directory, output_filename):
    # Main root of the XML file. All courses will be a node of this root.
    root = etree.Element('Products')

    for coursenumber in course_information_df.loc[:,'ID']:
    # Make a new node for the product
        new_product_node = etree.SubElement(root, 'Product')

        # Create the product: basic information about the course
        springest_create_product(parent = new_product_node,
                                 local_ID = coursenumber,
                                 table = course_information_df)

        # If the product has additional costs, add these with the additional info about these costs
        new_additional_costs = etree.Element('AdditionalCosts')
        new_product_node.insert(8, new_additional_costs)
        if course_information_df.loc[course_information_df.ID == coursenumber, 'AdditionalCosts'].values[0] != 0:
            new_additional_cost = etree.SubElement(new_additional_costs, 'AdditionalCost')

            springest_add_additional_costs(parent = new_additional_cost,
                                           local_ID = coursenumber,
                                           table = course_information_df)

        if sum(course_planning_df.ID.isin([coursenumber])) > 0: # if coursenumber is planned
            new_event = etree.SubElement(new_product_node, 'StartingDatePlaces')  # create a new node for all events of this course
        
            # Calculate a few variables that are needed for the schedules
            duration = course_information_df.loc[course_information_df.ID == coursenumber, 'Duration'].values[0] # duration of the course
            startdays_list = course_planning_df.loc[(course_planning_df.ID == coursenumber) & (course_planning_df.Day == '1'),'RowID'].reset_index(drop=True) # list of all the startdays of that course
            amount_startdays = len(startdays_list) # amount of startdays of that course
            # Create the schedules of the product
            springest_create_schedules(parent = new_event,
                            local_ID = coursenumber,
                            table_info = course_information_df,
                            table_planning = course_planning_df,
                            duration = duration,
                            startdays = startdays_list,
                            amount_startdays = amount_startdays )

        empty_nodes = pd.DataFrame({'nodename': ['Images', 'VideoEmbed', 'PriceExemptAmount', 'PriceAgreement', 'PriceInfo', 'Trainers', 'DurationAgreement',
                                                 'Runtime', 'ExtraInstructionsAfterBooking', 'ParticipantsAgreement', 'ContactPerson', 'AllowedSites', 
                                                 'Regions', 'Level', 'CrohoID', 'CreboID', 'PriceDiscounts', 'PePoints', 'Moments', 'CustomLtiParams'],
                                    'index': [3, 4, 9, 11, 14, 15, 19, 20, 22, 24, 27, 29, 30, 31, 32, 33, 34, 35, 36, 38]})

        for empty in empty_nodes.nodename:
            new_empty_node = etree.Element(empty)
            new_product_node.insert(empty_nodes.loc[empty_nodes.nodename == empty, 'index'].values[0], new_empty_node)

    # Make a tree of the main root with all its nodes and show it in the pretty XML style
    created_tree = etree.ElementTree(root)
    created_tree.write(open(os.path.join(output_directory, output_filename), 'wb'),
                      pretty_print=True, 
                      encoding = 'utf-8',
                      xml_declaration = True)