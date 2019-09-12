from lxml import etree
import pandas as pd
import os

import xml_general
import xml_springest

root = etree.Element('Products') # the main root of the XML

course_information_studytube = xml_general.read_course_information(directory = r'D:\Stack\Geo-ICT\Trainingen\repo\courses-xml',
                                                                   filename = 'Cursussen database.xlsx')

course_planning_studytube = xml_general.read_course_planning(directory = r'D:\Stack\Geo-ICT\Trainingen\repo\courses-xml',
                                                             filename = 'Cursussen database.xlsx')

course_information_studytube = course_information_studytube.rename(columns = { 'CursusID': 'ID',
                                                                        'Cursusnaam': 'Name',
                                                                        'Omschrijving': 'Description',
                                                                        'Prijs': 'TrainingPriceExVAT',
                                                                        'Extra_kosten': 'AdditionalCosts',
                                                                        'Omschrijving_extra_kosten': 'AdditionalCosts_description',
                                                                        'Categorie': 'Category',
                                                                        'Onderwerp': 'SubCategory',
                                                                        'Duur': 'Duration',
                                                                        'URL': 'WebAddress',
                                                                        'PDF_URL': 'PdfBrochure'})

course_planning_studytube = course_planning_studytube.rename(columns = {'CursusID': 'ID',
                                                                'Locatie': 'LocationName',
                                                                'Dag': 'Day',
                                                                'Datum': 'Date',
                                                                'Begintijd': 'StartTime',
                                                                'Eindtijd': 'EndTime'})

fixed_values = pd.DataFrame({'columnname': ['Language', 'VATPercentage', 'Certificate', 'TargetEducationalLevel'],
                                 'value': ['nl', '21', 'Certificaat opleider', 'HBO']})

for new_column in fixed_values.columnname:
    course_information_studytube[new_column] = fixed_values.loc[fixed_values.columnname == new_column, 'value'].values[0]

for rows in range(len(course_information_studytube)): # add the duration unit based on the Dutch value (dagen of weken)
    if course_information_studytube.loc[rows, 'Duur_eenheid'] == 'dagen':
        course_information_studytube.loc[rows, 'DurationUnit'] = 'days'
    elif course_information_studytube.loc[rows, 'Duur_eenheid'] == 'weken':
        course_information_studytube.loc[rows, 'DurationUnit'] = 'weeks'

course_information_studytube = course_information_studytube[['ID', 'Name', 'Description', 'TargetEducationalLevel', 'Language', 'TrainingPriceExVAT',
                                                             'VATPercentage', 'Certificate', 'AdditionalCosts', 'AdditionalCosts_description', 
                                                             'Category', 'SubCategory', 'Duration', 'DurationUnit', 'WebAddress', 'PdfBrochure']]

empty_nodes = pd.DataFrame({'nodename': ['Agenda', 'EducationalPoints', 'QualityMarks', 'Trainers', 'Discounts', 'RequiredUserFields'],
                            'index': [3, 9, 10, 12, 20, 21]})

for coursenumber in course_information_studytube.loc[:,'ID']:
    # Make a new node for the product
    new_product_node = etree.SubElement(root, 'Product')

    xml_springest.springest_create_product(parent = new_product_node,
                            local_ID = coursenumber,
                            table = course_information_studytube)

    new_additionalcosts = etree.Element('AdditionalCosts')
    new_product_node.insert(8, new_additionalcosts)

    if course_information_studytube.loc[course_information_studytube.ID == coursenumber, 'AdditionalCosts'].values[0] != 0:
        new_additional_costs = etree.SubElement(new_additionalcosts, 'AdditionalCost')

        new_additional_costs_type = etree.SubElement(new_additional_costs, 'Type')
        new_additional_costs_type.text = str(course_information_studytube.loc[course_information_studytube.ID == coursenumber, 'AdditionalCosts_description'].values[0])

        new_additional_costs_price = etree.SubElement(new_additional_costs, 'AdditionalCostPriceExVAT')
        new_additional_costs_price.text = str(course_information_studytube.loc[course_information_studytube.ID == coursenumber, 'AdditionalCosts'].values[0])

        new_additional_costs_VAT = etree.SubElement(new_additional_costs, 'VATPercentage')
        new_additional_costs_VAT.text = '21'


    new_schedule_type = etree.Element('ScheduleType')
    new_event = etree.SubElement(new_product_node, 'LiveSessions')  # create a new node for all events of this course

    if sum(course_planning_studytube.ID.isin([coursenumber])) > 0: # if coursenumber is planned
        new_schedule_type.text = 'scheduled'

        duration = course_information_studytube.loc[course_information_studytube.ID == coursenumber, 'Duration'].values[0] # duration of the course
        startdays = course_planning_studytube.loc[(course_planning_studytube.ID == coursenumber) & (course_planning_studytube.Day == '1'),'RowID'].reset_index(drop=True) # list of all the startdays of that course
        amount_startdays = len(startdays) # amount of startdays of that course

        for i in range(amount_startdays): # for the amount of startdays, add new Schedules
            new_event_child = etree.SubElement(new_event, 'LiveSession') # create a new node for the new event

            new_event_ID = etree.SubElement(new_event_child, 'ID')
            new_event_ID.text = 'EVENT_'+str(course_planning_studytube.loc[course_planning_studytube.RowID == startdays[i], 'EventID'].values[0])

            new_event_place = etree.SubElement(new_event_child, 'LocationName')
            new_event_place.text = 'kantoor '+ str(course_planning_studytube.loc[course_planning_studytube.RowID == startdays[i], 'LocationName'].values[0])

            new_event_address = etree.SubElement(new_event_child, 'Location')
            new_event_address.text = str(course_planning_studytube.loc[course_planning_studytube.RowID == startdays[i], 'LocationName'].values[0]) + ', the Netherlands'

            new_event_closed = etree.SubElement(new_event_child, 'LiveSessionClosed')
            new_event_closed.text = 'false'
       
            new_schedule = etree.SubElement(new_event_child, 'LiveSessionDates') # create the Schedule node
            for days in range(int(duration)): # for the duration of the course, add new Coursedays
                new_courseday = etree.SubElement(new_schedule, 'LiveSessionDate') # create the Courseday node 
                new_schedule_information = etree.SubElement(new_courseday, 'StartDate') # create the new node
                new_schedule_information.text = str(course_planning_studytube.loc[course_planning_studytube.RowID == str(int(startdays[i]) + days), 'Date'].values[0]) # indexing based on the unique RowID

                new_schedule_information = etree.SubElement(new_courseday, 'StartTime') # create the new node
                new_schedule_information.text = str(course_planning_studytube.loc[course_planning_studytube.RowID == str(int(startdays[i]) + days), 'StartTime'].values[0]) # indexing based on the unique RowID

                new_schedule_information = etree.SubElement(new_courseday, 'EndTime') # create the new node
                new_schedule_information.text = str(course_planning_studytube.loc[course_planning_studytube.RowID == str(int(startdays[i]) + days), 'EndTime'].values[0]) # indexing based on the unique RowID
        
    else:
        new_schedule_type.text = 'nodate'
    new_product_node.insert(15, new_schedule_type)
  
    
    for empty in empty_nodes.nodename:
        new_empty_node = etree.Element(empty)
        new_product_node.insert(empty_nodes.loc[empty_nodes.nodename == empty, 'index'].values[0], new_empty_node)

output_directory = r'D:\Stack\Geo-ICT\Trainingen\repo\courses-xml\output'
output_filename = 'output_studytube.xml'
created_tree = etree.ElementTree(root)
created_tree.write(open(os.path.join(output_directory, output_filename), 'wb'),
                    pretty_print=True, 
                    encoding = 'utf-8',
                    xml_declaration = True)
