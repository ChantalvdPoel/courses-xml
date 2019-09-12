###################################################################################
# Variables that can be changed by the user:
database_directory = r'D:\Stack\Geo-ICT\Trainingen\repo\courses-xml'
database_name = 'Cursussen database.xlsx'

output_directory = r'D:\Stack\Geo-ICT\Trainingen\repo\courses-xml\output'
output_name_geoict = 'cursusdatums.csv'

###################################################################################
import xml_general

# Reads the database: course information and the planning
print('De database aan het inlezen')
course_information = xml_general.read_course_information(directory = database_directory, filename = database_name)
course_planning = xml_general.read_course_planning(directory = database_directory, filename = database_name)

# Creates the geoict csv file for the website database
print('Het CSV bestand voor de Geo-ICT website aan het maken.')
#xml_general.create_cursusdatums_website(information_df = course_information, 
#                            planning_df = course_planning, 
#                            output_directory = output_directory,
#                            output_filename = output_name_geoict)

# List of the websites that need an XML
websites = ['springest', 'studytube', 'edubookers']

for website in websites:
    print('Bezig met de XML maken voor: ' + website)
    # Changing the format of the datafiles to the format needed for this specific XML file
    course_information_website = xml_general.course_information_adjusted(course_information, website)
    course_planning_website = xml_general.course_planning_adjusted(course_planning, website)

    # Creating the XML files based on the datafiles
    xml_general.create_xml_website(information_df = course_information_website,
                                   planning_df = course_planning_website,
                                   output_directory = output_directory,
                                   output_filename = 'output_' + website + '.xml',
                                   website = website)

print('Script is klaar. Alle bestanden zijn gemaakt.')



