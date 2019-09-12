from lxml import etree

import xml_general

course_information_edubookers = xml_general.read_course_information(directory = r'D:\Stack\Geo-ICT\Trainingen\repo\courses-xml',
                                                                   filename = 'Cursussen database.xlsx')

course_information_edubookers = xml_general.course_information_adjusted(course_information_edubookers, 'edubookers')

course_planning_edubookers = xml_general.read_course_planning(directory = r'D:\Stack\Geo-ICT\Trainingen\repo\courses-xml',
                                                             filename = 'Cursussen database.xlsx')

course_planning_edubookers = xml_general.course_planning_adjusted(course_planning_edubookers, 'edubookers')

def create_xml_edubookers(information_df, planning_df, output_directory, output_filename):
    root = etree.Element('trainings') 

    for coursenumber in course_information_edubookers.loc[:,'ID']:
        # Make a new node for the product
        new_product_node = etree.SubElement(root, 'training')

        xml_general.create_product( parent = new_product_node,
                                    coursenumber = coursenumber,
                                    information_df = information_df,
                                    website = 'edubookers')

        new_additional_costs = etree.Element('training_additional_costs')
        new_product_node.insert(5, new_additional_costs)
        new_additional_costs_description = etree.Element('training_additional_costs_description')
        new_product_node.insert(6, new_additional_costs_description)

        if course_information_edubookers.loc[course_information_edubookers.ID == coursenumber, 'Additional_costs'].values[0] != 0:
            new_additional_costs.text = str(course_information_edubookers.loc[course_information_edubookers.ID == coursenumber, 'Additional_costs'].values[0])
            new_additional_costs_description.text = str(course_information_edubookers.loc[course_information_edubookers.ID == coursenumber, 'Additional_costs_description'].values[0])

        new_event = etree.SubElement(new_product_node, 'training_items')  # create a new node for all events of this course

        if sum(course_planning_edubookers.ID.isin([coursenumber])) > 0: # if coursenumber is planned
            xml_general.create_schedules(parent = new_event,
                                            coursenumber = coursenumber,
                                            information_df = information_df,
                                            planning_df = planning_df,
                                            website = 'edubookers')
    xml_general.write_to_xml(root = root,
                             output_directory = output_directory,
                             output_filename = output_filename)

create_xml_edubookers(information_df = course_information_edubookers,
                      planning_df = course_planning_edubookers,
                      output_directory = r'D:\Stack\Geo-ICT\Trainingen\repo\courses-xml\output',
                      output_filename = 'output_edubookers_test.xml')