###################################################################################
# Variables that can be changed by the user:
database_directory = r'D:\Stack\Geo-ICT\Trainingen\repo\courses-xml'
database_name = 'Cursussen database.xlsx'

output_directory = r'D:\Stack\Geo-ICT\Trainingen\repo\courses-xml\output'
output_name_geoict = 'cursusdatums.csv'

###################################################################################
import functions

# Reads the database: course information and the planning
print('De database aan het inlezen')
course_information = functions.read_course_information(directory = database_directory, filename = database_name)
course_planning = functions.read_course_planning(directory = database_directory, filename = database_name)

# Checks the database if the data is correct
necessary_cols_info = ['Cursusnaam', 'CursusID', 'SpringestID', 'Omschrijving', 'Categorie', 'Onderwerp', 
                  'Duur', 'Duur_eenheid', 'Prijs', 'Extra_kosten', 'Omschrijving_extra_kosten', 'URL', 'PDF_URL', 'Test']
necessary_cols_planning = ['RowID', 'EventID', 'CursusID', 'Cursusnaam', 'Locatie', 'Dag', 'Datum', 'Begintijd', 'Eindtijd']

course_information_cols = course_information.columns.tolist()
course_planning_cols = course_planning.columns.tolist()

if all(elem in course_information_cols for elem in necessary_cols_info):
    print('Alle benodigde kolommen uit de cursusinformatie zijn aanwezig')
else:
    missing = list(set(necessary_cols_info) - set(course_information_cols))

    raise ValueError('Er missen kolommen in de cursusinformatie, namelijk: ' + str(missing))


if all(elem in course_planning_cols for elem in necessary_cols_planning):
    print('Alle benodigde kolommen uit de cursusplanning zijn aanwezig')
else:
    missing = list(set(necessary_cols_planning) - set(course_planning_cols))

    raise ValueError()

# Creates the geoict csv file for the website database
print('Het CSV bestand voor de Geo-ICT website aan het maken.')
functions.create_cursusdatums_website(information_df = course_information, 
                            planning_df = course_planning, 
                            output_directory = output_directory,
                            output_filename = output_name_geoict)

# List of the websites that need an XML
websites = ['springest', 'studytube', 'edubookers']

for website in websites:
    print('Bezig met de XML maken voor: ' + website)
    # Changing the format of the datafiles to the format needed for this specific XML file
    course_information_website = functions.course_information_adjusted(course_information, website)
    course_planning_website = functions.course_planning_adjusted(course_planning, website)

    # Creating the XML files based on the datafiles
    functions.create_xml_website(information_df = course_information_website,
                                   planning_df = course_planning_website,
                                   output_directory = output_directory,
                                   output_filename = 'output_' + website + '.xml',
                                   website = website)

print('Script is klaar. Alle bestanden zijn gemaakt.')



