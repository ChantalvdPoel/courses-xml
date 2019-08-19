# Import all necessary modules
from lxml import etree # lxml is being used instead of ElementTree because lxml can use CDATA which is necessary for this particular XML file
import sys 
import pandas as pd
import numpy as np
from datetime import datetime

sys.path.append(r'C:\Users\chant\source\repos\XML writer cursusaanbod')
import read_courseinfo_springest as reader
testdata = reader.read_courseinfo_springest()

extra_info = pd.DataFrame({'columnname': ['Language', 'VatIncluded', 'PricePeriod', 'PriceComplete',
                                          'CourseType', 'Completion', 'MaxParticipants', 'ProductType'],
                           'value': ['nl', 'no', 'all', 'true', 'course', 'Certificaat', '8', 'open']})

for new_column in extra_info.columnname:
    testdata[new_column] = extra_info.loc[extra_info.columnname == new_column, 'value'].values[0]

# The amount of VAT needs to be calculated per course, so this is added individually
testdata['VatAmount'] = testdata.Price.apply(lambda x: str(int(x)*0.21))

# Fill the DurationUnit column based on the Dutch value
for rows in range(len(testdata)):
    if testdata.loc[rows, 'Duration_unit'] == 'dagen':
        testdata.loc[rows, 'DurationUnit'] = 'days'
    elif testdata.loc[rows, 'Duration_unit'] == 'weken':
        testdata.loc[rows, 'DurationUnit'] = 'weeks'

testdata = testdata[['ID', 'Description', 'Name', 'Language', 'Price', 'VatIncluded', 'VatAmount', 
                     'PricePeriod', 'AdditionalCosts', 'PriceComplete', 'CourseType', 'Duration', 
                     'DurationUnit', 'Completion', 'MaxParticipants', 'WebAddress', 'PdfBrochure', 'ProductType']]

# Main root of the XML file. All courses will be a node of this root.
root = etree.Element('Products')

# Pandas dataframe with some testdata of basic information about the courses
#testdata = pd.DataFrame({   'ID': ['001', '002'],
 #                           'Description': ['Dit is de eerste cursus', 'Dit is de tweede cursus'],
 #                           'Name': ['AutoCAD 2D Basis', 'ArcGIS 2D Basis'],
  ##                          'Price': [795, 995],
 #                           'Duration': [3, 3],
   #                         'Additional_costs': [0, 10]})



#testdatums = pd.DataFrame({ 'RowID': [1, 2, 3, 4, 5, 6, 7, 8, 9],
#                            'ID': ['001',  '001', '001', '001',  '001', '001','002', '002', '002'],
#                            'Place': ['Apeldoorn', 'Apeldoorn', 'Apeldoorn', 'Amsterdam', 'Amsterdam', 'Amsterdam', 'Rotterdam', 'Rotterdam', 'Rotterdam'],
#                            'Day': [1, 2, 3, 1, 2, 3, 1, 2, 3],
#                            'Date': ['01-01-2019', '02-01-2019', '03-01-2019', '01-07-2019', '02-07-2019', '03-07-2019', '02-02-2019', '04-02-2019', '06-02-2019']})

testdatums = pd.read_excel('D:\Stack\Geo-ICT\Trainingen\Cursussen database V7.xlsx',
                           sheet_name = 'planning',
                           dtype = str)

testdatums.rename(columns = {'CursusID': 'ID',
                             'Locatie': 'Place',
                             'Dag': 'Day',
                             'Datum': 'Date',
                             'Begintijd': 'StartTime',
                             'Eindtijd': 'EndTime'}, inplace = True)

# Convert date notation
date_to_datetime = [datetime.strptime(str(testdatums.Date[idx]), '%d-%m-%Y') for idx in range(len(testdatums))]
testdatums.Date = [date_to_datetime[idx].strftime('%Y-%m-%d') for idx in range(len(date_to_datetime))]

# Convert time notation
starttime_to_datetime = [datetime.strptime(str(testdatums.StartTime[idx]), '%H:%M:%S') for idx in range(len(testdatums))]
testdatums.StartTime = [starttime_to_datetime[idx].strftime('%H:%M') for idx in range(len(starttime_to_datetime))]
endtime_to_datetime = [datetime.strptime(str(testdatums.EndTime[idx]), '%H:%M:%S') for idx in range(len(testdatums))]
testdatums.EndTime = [endtime_to_datetime[idx].strftime('%H:%M') for idx in range(len(endtime_to_datetime))]


def add_product_information(parent, local_ID, information_type, table):
    # Will create nodes with some information for each course
    new_product_information = etree.SubElement(parent, information_type) # create the new node
    new_product_information.text = str(table[table.ID == local_ID][information_type].values[0]) # indexing based on the unique course ID number

def create_product(parent, local_ID, table):
    # Will add all the courses to the Products root as new nodes
    # Makes use of the create_basic_information function to provide all the basic information for every course
    for colname in table.columns.tolist(): # for every column in the table with basic information, do this function
        if (table.loc[table.ID == local_ID, colname].values[0] != 0): # only add information if it is available (not 0)
            if (colname == 'Name') | (colname == 'Description'): # if it's a name of description, use CDATA instead or a regular string
                new_product_information = etree.SubElement(parent, colname) # create the new node
                new_product_information.text = etree.CDATA(table[table.ID == local_ID][colname].values[0]) # indexing based on the unique course ID number
            elif (colname == 'AdditionalCosts'):
                continue
            else:
                add_product_information(parent = parent, 
                                   local_ID = local_ID, 
                                   information_type = colname,
                                   table = table)

def add_courseday_information(parent, schedule_information, daynumber, table, startday_index):
    # Will add the information from the coursedays to the schedule
    new_schedule_information = etree.SubElement(parent, schedule_information) # create the new node
    new_schedule_information.text = str(table.loc[table.RowID == str(int(startday_index) + daynumber), schedule_information].values[0]) # indexing based on the unique RowID

def create_schedules(parent, local_ID, table_info, table_planning, duration, startdays, amount_startdays):
    # Will create the nodes with information about the planning including the schedule with all the coursedays
    for i in range(amount_startdays): # for the amount of startdays, add new Schedules
        new_event_child = etree.SubElement(parent, 'StartingDatePlace') # create a new node for the new event

        new_event_ID = etree.SubElement(new_event_child, 'ID')
        new_event_ID.text = local_ID

        new_event_startdate = etree.SubElement(new_event_child, 'Startdate')
        new_event_startdate.text = str(table_planning.loc[table_planning.RowID == startdays_list[i], 'Date'].values[0])

        new_event_enddate = etree.SubElement(new_event_child, 'Enddate')
        new_event_enddate.text = str(table_planning.loc[table_planning.RowID == str(int(startdays_list[i]) + int(duration) - 1), 'Date'].values[0])

        new_event_place = etree.SubElement(new_event_child, 'Place')
        new_event_place.text = str(table_planning.loc[table_planning.RowID == startdays_list[i], 'Place'].values[0])

        new_event_startdateismonth = etree.SubElement(new_event_child, 'StartdateIsMonthOnly')
        new_event_startdateismonth.text = 'false'

        new_event_enddateismonth = etree.SubElement(new_event_child, 'EnddateIsMonthOnly')
        new_event_enddateismonth.text = 'false'

        new_event_startguaranteed = etree.SubElement(new_event_child, 'StartGuaranteed')
        new_event_startguaranteed.text = 'true'

        new_schedule = etree.SubElement(new_event_child, 'Schedule') # create the Schedule node
        for days in range(int(duration)): # for the duration of the course, add new Coursedays
            new_courseday = etree.SubElement(new_schedule, 'Courseday') # create the Courseday node 
            for colname in ['Date', 'Place', 'StartTime', 'EndTime']: # for every column with planning information, add this to the Courseday node
                add_courseday_information(  parent = new_courseday, 
                                            schedule_information = colname, 
                                            daynumber = days,
                                            table = table_planning,
                                            startday_index = startdays_list[i])
            name_courseday = etree.Element('Name')
            name_courseday.text = etree.CDATA('Cursusdag ' + str(days+1))
            new_courseday.insert(3, name_courseday)


def add_additional_costs(parent, local_ID, table):
    # if there are any additional costs, add a new node to include these
    new_additional_costs = etree.SubElement(parent, 'AdditionalCost')
    new_additional_costs_type = etree.SubElement(new_additional_costs, 'Type')
    new_additional_costs_type.text = 'study material'
    new_additional_costs_price = etree.SubElement(new_additional_costs, 'Price')
    new_additional_costs_price.text = str(table.loc[table.ID == local_ID, 'AdditionalCosts'].values[0])
    new_additional_costs_vatincluded = etree.SubElement(new_additional_costs, 'VatIncluded')
    new_additional_costs_vatincluded.text = 'no'
    new_additional_costs_vatamount = etree.SubElement(new_additional_costs, 'VatAmount')
    new_additional_costs_vatamount.text = str(int(table.loc[table.ID == local_ID, 'AdditionalCosts'].values[0])*0.21)
    new_additional_costs_mandatory = etree.SubElement(new_additional_costs, 'Mandatory')
    new_additional_costs_mandatory.text = 'true'

# For every course in the database, create a new node with all the basic information
for coursenumber in testdata.loc[:,'ID']:
    # Make a new node for the product
    new_product_node = etree.SubElement(root, 'Product')

    # Create the product: basic information about the course
    create_product(parent = new_product_node,
                   local_ID = coursenumber,
                   table = testdata)

    # If the product has additional costs, add these with the additional info about these costs
    if testdata.loc[testdata.ID == coursenumber, 'AdditionalCosts'].values[0] != 0:
        new_additionalcosts = etree.Element('AdditionalCosts')
        new_product_node.insert(8, new_additionalcosts)
        #new_additionalcosts = etree.SubElement(new_product_node, 'AdditionalCosts')
        add_additional_costs(parent = new_additionalcosts,
                             local_ID = coursenumber,
                             table = testdata)

    if sum(testdatums.ID.isin([coursenumber])) > 0: # if coursenumber is planned
        new_event = etree.SubElement(new_product_node, 'StartingDatePlaces')  # create a new node for all events of this course
        
        # Calculate a few variables that are needed for the schedules
        duration = testdata.loc[testdata.ID == coursenumber, 'Duration'].values[0] # duration of the course
        startdays_list = testdatums.loc[(testdatums.ID == coursenumber) & (testdatums.Day == '1'),'RowID'].reset_index(drop=True) # list of all the startdays of that course
        amount_startdays = len(startdays_list) # amount of startdays of that course
        # Create the schedules of the product
        create_schedules(   parent = new_event,
                            local_ID = coursenumber,
                            table_info = testdata,
                            table_planning = testdatums,
                            duration = duration,
                            startdays = startdays_list,
                            amount_startdays = amount_startdays )

# Make a tree of the main root with all its nodes and show it in the pretty XML style
created_tree = etree.ElementTree(root)
created_tree.write(open('D:\Stack\Geo-ICT\Trainingen\\repo\courses-xml\\result.xml', 'wb'),
                  pretty_print=True, 
                  encoding = 'utf-8',
                  xml_declaration = True)



