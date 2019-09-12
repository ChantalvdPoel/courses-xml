from lxml import etree
import pandas as pd
import os

import xml_general
import xml_springest

root = etree.Element('trainings') # the main root of the XML

course_information_edubookers = xml_general.read_course_information(directory = r'D:\Stack\Geo-ICT\Trainingen\repo\courses-xml',
                                                                   filename = 'Cursussen database.xlsx')

course_planning_edubookers = xml_general.read_course_planning(directory = r'D:\Stack\Geo-ICT\Trainingen\repo\courses-xml',
                                                             filename = 'Cursussen database.xlsx')

course_information_edubookers = course_information_edubookers.rename(columns = { 'CursusID': 'ID',
                                                                        'Cursusnaam': 'Name',
                                                                        'Omschrijving': 'Description',
                                                                        'Extra_kosten': 'Additional_costs',
                                                                        'Omschrijving_extra_kosten': 'Additional_costs_description',
                                                                        'Max_deelnemers': 'Max_participants'})

course_planning_edubookers = course_planning_edubookers.rename(columns = {'CursusID': 'ID',
                                                                        'Locatie': 'Location',
                                                                        'Dag': 'Day',
                                                                        'Datum': 'Date',
                                                                        'Begintijd': 'Time_start',
                                                                        'Eindtijd': 'Time_end'})

fixed_values = pd.DataFrame({'columnname': ['Type', 'Complete'],
                                 'value': ['open', 'certificaat']})

for new_column in fixed_values.columnname:
    course_information_edubookers[new_column] = fixed_values.loc[fixed_values.columnname == new_column, 'value'].values[0]


for rows in range(len(course_information_edubookers)): # add the duration unit based on the Dutch value (dagen of weken)
    if course_information_edubookers.loc[rows, 'Duur_eenheid'] == 'weken':
        course_information_edubookers.loc[rows, 'Days'] = str(int(course_information_edubookers.loc[rows, 'Duur']) * 7)
    elif course_information_edubookers.loc[rows, 'Duur_eenheid'] == 'dagen':
        course_information_edubookers.loc[rows, 'Days'] = course_information_edubookers.loc[rows, 'Duur']

prijs_en_duur = course_information_edubookers[['ID', 'Prijs', 'Duur']]
course_information_edubookers = course_information_edubookers[['ID', 'Type', 'Name', 'Description', 'Days', 'Additional_costs',
                                                             'Additional_costs_description', 'Max_participants', 'Complete']]

for coursenumber in course_information_edubookers.loc[:,'ID']:
    # Make a new node for the product
    new_product_node = etree.SubElement(root, 'training')

    xml_springest.springest_create_product( parent = new_product_node,
                                            local_ID = coursenumber,
                                            table = course_information_edubookers,
                                            edubookers = True)

    new_additional_costs = etree.Element('training_additional_costs')
    new_product_node.insert(5, new_additional_costs)
    new_additional_costs_description = etree.Element('training_additional_costs_description')
    new_product_node.insert(6, new_additional_costs_description)

    if course_information_edubookers.loc[course_information_edubookers.ID == coursenumber, 'Additional_costs'].values[0] != 0:
        new_additional_costs.text = str(course_information_edubookers.loc[course_information_edubookers.ID == coursenumber, 'Additional_costs'].values[0])
        new_additional_costs_description.text = str(course_information_edubookers.loc[course_information_edubookers.ID == coursenumber, 'Additional_costs_description'].values[0])

    new_event = etree.SubElement(new_product_node, 'training_items')  # create a new node for all events of this course

    if sum(course_planning_edubookers.ID.isin([coursenumber])) > 0: # if coursenumber is planned
        duration = prijs_en_duur.loc[prijs_en_duur.ID == coursenumber, 'Duur'].values[0] # duration of the course
        startdays = course_planning_edubookers.loc[(course_planning_edubookers.ID == coursenumber) & (course_planning_edubookers.Day == '1'),'RowID'].reset_index(drop=True) # list of all the startdays of that course
        amount_startdays = len(startdays) # amount of startdays of that course

        for i in range(amount_startdays): # for the amount of startdays, add new Schedules
                new_event_child = etree.SubElement(new_event, 'training_item') # create a new node for the new event

                new_event_startguaranteed = etree.SubElement(new_event_child, 'training_item_startassurance')
                new_event_startguaranteed.text = 'false'

                new_event_startdate = etree.SubElement(new_event_child, 'training_item_startdate')
                new_event_startdate.text = str(course_planning_edubookers.loc[course_planning_edubookers.RowID == startdays[i], 'Date'].values[0])

                new_event_starttime = etree.SubElement(new_event_child, 'training_item_time_start')
                new_event_starttime.text = str(course_planning_edubookers.loc[course_planning_edubookers.RowID == startdays[i], 'Time_start'].values[0])

                new_event_endtime = etree.SubElement(new_event_child, 'training_item_time_end')
                new_event_endtime.text = str(course_planning_edubookers.loc[course_planning_edubookers.RowID == startdays[i], 'Time_end'].values[0])

                new_schedule = etree.SubElement(new_event_child, 'training_item_followup') # create the Schedule node
                for days in range(1, int(duration)): # for the duration of the course, add new Coursedays
                    new_schedule_information = etree.SubElement(new_schedule, 'training_item_followup_date') # create the new node
                    new_schedule_information.text = str(course_planning_edubookers.loc[course_planning_edubookers.RowID == str(int(startdays[i]) + days), 'Date'].values[0]) # indexing based on the unique RowID

                    new_schedule_information = etree.SubElement(new_schedule, 'training_item_followup_start') # create the new node
                    new_schedule_information.text = str(course_planning_edubookers.loc[course_planning_edubookers.RowID == str(int(startdays[i]) + days), 'Time_start'].values[0]) # indexing based on the unique RowID

                    new_schedule_information = etree.SubElement(new_schedule, 'training_item_followup_end') # create the new node
                    new_schedule_information.text = str(course_planning_edubookers.loc[course_planning_edubookers.RowID == str(int(startdays[i]) + days), 'Time_end'].values[0]) # indexing based on the unique RowID
        
                new_event_place = etree.SubElement(new_event_child, 'training_item_location')
                new_event_place.text = str(course_planning_edubookers.loc[course_planning_edubookers.RowID == startdays[i], 'Location'].values[0])

                new_event_price = etree.SubElement(new_event_child, 'training_item_price')
                new_event_price.text = str(prijs_en_duur.loc[prijs_en_duur.ID == coursenumber, 'Prijs'].values[0])

output_directory = r'D:\Stack\Geo-ICT\Trainingen\repo\courses-xml\output'
output_filename = 'output_edubookers.xml'
created_tree = etree.ElementTree(root)
created_tree.write(open(os.path.join(output_directory, output_filename), 'wb'),
                    pretty_print=True, 
                    encoding = 'utf-8',
                    xml_declaration = True)
