# Import all necessary modules
from lxml import etree # lxml is being used instead of ElementTree because lxml can use CDATA which is necessary for this particular XML file
import sys 
import pandas as pd

# Main root of the XML file. All courses will be a node of this root.
root = etree.Element('Products')

# Pandas dataframe with some testdata of basic information about the courses
testdata = pd.DataFrame({   'ID': ['001', '002'],
                            'Description': ['Dit is de eerste cursus', 'Dit is de tweede cursus'],
                            'Name': ['AutoCAD 2D Basis', 'ArcGIS 2D Basis'],
                            'Price': [795, 995],
                            'Duration': [3, 3]})

testdatums = pd.DataFrame({ 'RowID': [1, 2, 3, 4, 5, 6, 7, 8, 9],
                            'ID': ['001',  '001', '001', '001',  '001', '001','002', '002', '002'],
                            'Place': ['Apeldoorn', 'Apeldoorn', 'Apeldoorn', 'Amsterdam', 'Amsterdam', 'Amsterdam', 'Rotterdam', 'Rotterdam', 'Rotterdam'],
                            'Day': [1, 2, 3, 1, 2, 3, 1, 2, 3],
                            'Date': ['01-01-2019', '02-01-2019', '03-01-2019', '01-07-2019', '02-07-2019', '03-07-2019', '02-02-2019', '04-02-2019', '06-02-2019']})

def create_information(parent, local_ID, information_type, table):
    # Will create nodes with some information for each course
    new_product_information = etree.SubElement(parent, information_type) # create the new node
    new_product_information.text = str(table[table.ID == local_ID][information_type].values[0]) # fill the node with the appropiate data

def create_product(parent, local_ID, table):
    # Will add all the courses to the Products root as new nodes
    # Makes use of the create_basic_information function to provide all the basic information for every course
    
    for colname in table.columns.tolist(): # for every column in the table with basic information, do this function
        create_information(parent = parent, 
                           local_ID = local_ID, 
                           information_type = colname,
                           table = table)

def create_planning_info(parent, local_ID, table_info, table_planning):
    # Voegt de vaste waarden toe van de planning:
        # Startdatum, Einddatum, Plaats
    new_dateplace_node = etree.SubElement(parent, 'StartingDatePlace')

    duration = table_info.loc[table_info.ID == local_ID, 'Duration'].values[0]
    # Voegt een schedule node toe
       
    startdays_list = table_planning.loc[(table_planning.ID == local_ID) & (table_planning.Day == 1),'RowID'].reset_index(drop=True)
  
    amount_startdays = len(startdays_list)

    for i in range(amount_startdays):
        new_schedule = etree.SubElement(new_dateplace_node, 'Schedule')
        # Voor het aantal cursusdagen: voer create_schedule() uit
    
        for days in range(duration):
            new_courseday = etree.SubElement(new_schedule, 'Courseday')
            for colname in table_planning.columns.tolist():
                create_schedule(parent = new_courseday, 
                                schedule_information = colname, 
                                daynumber = days,
                                table = table_planning,
                                startday_index = startdays_list[i])

def create_schedule(parent, schedule_information, daynumber, table, startday_index):
    # Voegt de cursusdagen toe aan de schedule node
    # Vaste waarden: Datum, Plaats, Naam, Begintijd, Eindtijd
    new_schedule_information = etree.SubElement(parent, schedule_information)
    new_schedule_information.text = str(table.loc[table.RowID == startday_index + daynumber, schedule_information].values[0])


# For every course in the database, create a new node with all the basic information
for coursenumber in testdata.loc[:,'ID']:
    new_product_node = etree.SubElement(root, 'Product')

    create_product(parent = new_product_node,
                   local_ID = coursenumber,
                   table = testdata)

    new_date_parent = etree.SubElement(new_product_node, 'StartingDatePlaces')  

    create_planning_info(parent = new_date_parent,
                         local_ID = coursenumber,
                         table_info = testdata,
                         table_planning = testdatums)

# Make a tree of the main root with all its nodes and show it in the pretty XML style
created_tree = etree.ElementTree(root)
created_tree.write(sys.stdout, pretty_print=True)
