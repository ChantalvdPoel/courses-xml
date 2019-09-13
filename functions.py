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
    course_information = pd.read_excel(os.path.join(directory, filename), sheet_name = 'cursussen', dtype=str)
    course_information.fillna(0, inplace = True)

    return course_information

def course_information_adjusted(information_df, website):
    """
    This function will transform the course information dateframe to a format that can be used to make the specific XML
    The function will:
        - change the column names to the names that are used in the nodes
        - add columns with fixed values
        - order the columns in the order of the nodes in the XSD
    """
    # Make a copy of the original datafile
    df = information_df.copy()

    if website == 'springest':
        # Changing columnnames to the names used in the XML
        columnnames = {'CursusID': 'ID', 
                       'Cursusnaam': 'Name', 
                       'Omschrijving': 'Description',
                       'Prijs': 'Price', 
                       'Extra_kosten': 'AdditionalCosts', 
                       'Omschrijving_extra_kosten': 'AdditionalCosts_description',
                       'Duur': 'Duration', 
                       'Max_deelnemers': 'MaxParticipants',
                       'URL': 'WebAddress', 
                       'PDF_URL': 'PdfBrochure'}

        # Adding variables with a fixed value
        fixed_values = pd.DataFrame({'columnname': ['Language', 'VatIncluded', 'PricePeriod', 'PriceComplete',
                                                'CourseType', 'Completion', 'ProductType'],
                                     'value': ['nl', 'no', 'all', 'true', 'course', 'Certificaat', 'open']})

        # Add the VAT amount (BTW bedrag)
        df['VatAmount'] = df.Prijs.apply(lambda x: str(round((int(x)*0.21),2))) 

        # Adds the duration unit based on the Dutch value (dagen of weken)
        for rows in range(len(df)): 
            if df.loc[rows, 'Duur_eenheid'] == 'dagen':
                df.loc[rows, 'DurationUnit'] = 'days'
            elif df.loc[rows, 'Duur_eenheid'] == 'weken':
                df.loc[rows, 'DurationUnit'] = 'weeks'
        
        # List with the columnnames in the order as they need to appear in the XML
        order = ['ID', 'Name', 'Description', 'Language', 'Price', 
                'VatIncluded', 'VatAmount', 'PricePeriod', 
                'AdditionalCosts', 'PriceComplete', 'CourseType', 
                'Duration', 'DurationUnit', 'Completion', 
                'MaxParticipants', 'WebAddress', 'PdfBrochure', 'ProductType']

    elif website == 'studytube':
        # Changing columnnames to the names used in the XML
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

        # Adding variables with a fixed value
        fixed_values = pd.DataFrame({'columnname': ['Language', 'VATPercentage', 'Certificate', 'TargetEducationalLevel'],
                                     'value': ['nl', '21', 'Certificaat opleider', 'HBO']})
        
        # Adds the duration unit based on the Dutch value (dagen of weken)
        for rows in range(len(df)):
            if df.loc[rows, 'Duur_eenheid'] == 'dagen':
                df.loc[rows, 'DurationUnit'] = 'days'
            elif df.loc[rows, 'Duur_eenheid'] == 'weken':
                df.loc[rows, 'DurationUnit'] = 'weeks'
        
        # List with the columnnames in the order as they need to appear in the XML
        order = ['ID', 'Name', 'Description', 'TargetEducationalLevel', 'Language', 'TrainingPriceExVAT',
                 'VATPercentage', 'Certificate', 'AdditionalCosts', 'AdditionalCosts_description', 
                 'Category', 'SubCategory', 'Duration', 'DurationUnit', 'WebAddress', 'PdfBrochure']

    elif website == 'edubookers':
        # Changing columnnames to the names used in the XML
        columnnames = {'CursusID': 'ID',
                       'Cursusnaam': 'Name',
                       'Omschrijving': 'Description',
                       'Extra_kosten': 'Additional_costs',
                       'Omschrijving_extra_kosten': 'Additional_costs_description',
                       'Max_deelnemers': 'Max_participants',
                       'Duur': 'Duration',
                       'Prijs': 'Price'}

        # Adding variables with a fixed value
        fixed_values = pd.DataFrame({'columnname': ['Type', 'Complete'],
                                     'value': ['open', 'certificaat']})

        # Adds the duration unit based on the Dutch value (dagen of weken)
        for rows in range(len(df)): 
            if df.loc[rows, 'Duur_eenheid'] == 'weken':
                df.loc[rows, 'Days'] = str(int(df.loc[rows, 'Duur']) * 7)
            elif df.loc[rows, 'Duur_eenheid'] == 'dagen':
                df.loc[rows, 'Days'] = df.loc[rows, 'Duur']
        
                # List with the columnnames in the order as they need to appear in the XML
        order = ['ID', 'Type', 'Name', 'Description', 'Days', 'Additional_costs',
                 'Additional_costs_description', 'Max_participants', 'Complete', 'Duration', 'Price']

    else:
        raise ValueError('dit is geen correcte website, kies uit: springest, studytube of edubookers')

    # Change the column names to the names that are used in the nodes (in the XSD)
    df.rename(columns = columnnames, inplace = True)

    # Add columns with fixed values
    for col in fixed_values.columnname:
        df[col] = fixed_values.loc[fixed_values.columnname == col, 'value'].values[0]

    # Order the columns following the order in of the list
    df = df[order]
           
    return df

def read_course_planning(directory, filename):
    """ 
    This function will read the database file and returns the planning of the courses in a pandas dataframe
    ! Every value will be read as a string
    """
    course_planning = pd.read_excel(os.path.join(directory, filename),
                                    sheet_name = 'planning',
                                    dtype = str)
    # Convert time notation
    for tijd in ['Begintijd', 'Eindtijd']:
        string_to_datetime = [datetime.strptime(str(course_planning.loc[idx, tijd]), '%H:%M:%S') for idx in range(len(course_planning))]
        course_planning[tijd] = [string_to_datetime[idx].strftime('%H:%M') for idx in range(len(string_to_datetime))]

    return course_planning

def course_planning_adjusted(planning_df, website):
    """
    This function will transform the course planning dateframe to a format that can be used to make the Springest XML
    The function will:
        - change the column names to the names that are used in the nodes
    """
    df = planning_df.copy()

    if website == 'springest':
        # Dictionaries with the conversions of the column names, depending on the website
        columnnames = {'CursusID': 'ID',
                       'Locatie': 'Place',
                       'Dag': 'Day',
                       'Datum': 'Date',
                       'Begintijd': 'StartTime',
                       'Eindtijd': 'EndTime'}

    elif website == 'studytube':
        columnnames = {'CursusID': 'ID',
                       'Locatie': 'LocationName',
                       'Dag': 'Day',
                       'Datum': 'Date',
                       'Begintijd': 'StartTime',
                       'Eindtijd': 'EndTime'}

    elif website == 'edubookers':
        columnnames = {'CursusID': 'ID',
                       'Locatie': 'Location',
                       'Dag': 'Day',
                       'Datum': 'Date',
                       'Begintijd': 'Time_start',
                       'Eindtijd': 'Time_end'}
    else:
        raise ValueError('dit is geen correcte website, kies uit: springest, studytube of edubookers')

    # Changing the column names to the names used in the XML
    df.rename(columns = columnnames, inplace = True)
    
    return df

def add_information_from_df(parent, df):
    """
    This function will add the information from a dataframe to the parent
    df must have two columns, one column 'type' with all the names of the nodes that need to be added and one column 'value' with all values of the nodes
    """
    for type in df.type:
        new_node = etree.SubElement(parent, type)
        new_node.text = df.loc[df.type == type, 'value'].values[0]

def add_product_information(parent, coursenumber, information_type, information_df, website):
    """
    This function will add all the information that is in the information_df
    """
    if website == 'edubookers':
        if (information_type != 'Duration') & (information_type != 'Price'): # for edubookers, skip the Duration and Price column, they do not need to be included in this part
            new_product_information = etree.SubElement(parent, 'training_'+information_type.lower()) # every node in Edubookers needs to start with 'training_.....'
            new_product_information.text = str(information_df.loc[information_df.ID == coursenumber, information_type].values[0]) 
    elif (website == 'springest') | (website == 'studytube'): # for springest and studytube, all columns that are in the information_df can be added in this part
        new_product_information = etree.SubElement(parent, information_type) 
        new_product_information.text = str(information_df.loc[information_df.ID == coursenumber, information_type].values[0])
    else:
        raise ValueError('dit is geen correcte website, kies uit: springest, studytube of edubookers')

def add_courseday_information(parent, schedule_information, daynumber, planning_df, startday_index):
    """
    This function will add all the basic information that is in the planning_df (not the planning itself, but things like locations and startdates)
    """
    new_schedule_information = etree.SubElement(parent, schedule_information) 
    new_schedule_information.text = str(planning_df.loc[planning_df.RowID == str(int(startday_index) + daynumber), schedule_information].values[0]) 

def create_geoict_df(information_df, planning_df):
    """
    This function creates the dataframe that is used for the website (geo-ict.nl) database
    The dataframe contains the ID, coursname, a sentence with the coursename+dates+location, the startdate, location
    These sentences are used to fill the forms on the website when you want to apply for a course
    """
    geoict_df = pd.DataFrame(columns = ['id', 'cursusnaam', 'tekst', 'datum', 'locatie']) # initialisation of the needed dataframe
    # dataframe with month in numbers and letters for conversion
    months = pd.DataFrame({'numbers': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12],
                            'letters': ['januari', 'februari', 'maart', 'april', 'mei', 'juni',
                                        'juli', 'augustus', 'september', 'oktober', 'november', 'december']})

    # an event is defined as every time a course is planned, from the startdate to the enddate
    # so if course1 is planned on 1, 2 and 3 January and again on 1, 2 and 3 February, then this course has two events, where event1 = 1,2,3 January and event2 = 1,2,3 February
    count_events = len(pd.unique(planning_df.EventID))
    for event_idx in range(count_events): # for every event that is in the planning
        event_ID =  pd.unique(planning_df.EventID)[event_idx] # the event ID
        geoict_df.loc[event_idx, 'id'] = event_ID # fill in the event ID in the geoict dataframe

        course_ID = planning_df.loc[planning_df.EventID == event_ID, 'CursusID'].values[0] # the course ID
        event_place = planning_df.loc[planning_df.EventID == event_ID, 'Locatie'].values[0] # the place where the course is given

        coursename =  information_df.loc[information_df.CursusID == course_ID, 'Cursusnaam'].values[0] # the coursename
        geoict_df.loc[event_idx, 'cursusnaam'] = coursename # fill in the coursenames in the geoict dataframe

        dates = planning_df.loc[planning_df.EventID == event_ID, 'Datum'].tolist() # all dates of this event in a list

        geoict_df.loc[event_idx, 'datum'] = dates[0] # the 'datum' in the geoict dataframe is the startdate, so the first date in the list

        dates = [datetime.strptime(date, "%Y-%m-%d") for date in dates] # convert the string dates to datetime objects

        # a list of all months the event is planned in, needed if the event takes place in multiple months, occurs sometimes
        # if the course is very long or it is planned at the end of one month and the start of the next month
        event_months = pd.unique([str(int(date.strftime("%m"))) for date in dates])

        # the column "tekst" is defined as the column with a string that combines the coursename, the dates and the location as a sentence
        # the text is used for the website where users can choose an event of the course
        if len(event_months) == 1: # als alle dagen in dezelfde maand vallen
            # the str(int()) combination is used multiple times to make sure the 01-09 numbers as used in the datetime objects are written as 1-9 numbers
            days_string = ', '.join([str(int(date.strftime("%d"))) for date in dates]) # join all days to one string
            month = months.loc[months.numbers == int(dates[-1].strftime("%m")), 'letters'].values[0] # get the month in letters
            days_string = days_string + " " + str(month) # combine the days-string with the month
            text = coursename + ": " + days_string # combine the coursename with the days and the month to get the string that is needed

        else: # if the course takes place in multiple months, something else needs to happen
            days_string = "" # make an empty string for initialisation

            for m in event_months: # for every month that the event is planned in...
                date_subset = [date for date in dates if str(int(date.month)) == m] # make a subset of the dates that are in the current month
                days_string = days_string + ', '.join([str(int(date.strftime("%d"))) for date in date_subset]) # add the days of this subset to the string
                month = months.loc[months.numbers == int(m), 'letters'].values[0] # get the current month in letters
                days_string = days_string + " " + str(month) + " & " # add the month to the string

            text = coursename + ": " + days_string[:-3] # if the loop is finished, there is one too many " & " added to the string, so this is removed by using the string up until the last 3 characters
        
        text = text + " in " + event_place 
        geoict_df.loc[event_idx, 'tekst'] = text # fill in the text in the geoict dataframe

        geoict_df.loc[event_idx, 'locatie'] = event_place

    # add the courses to the dataframe that are on call (op afroep) 
    courses_calls = information_df.loc[information_df.Frequentie == 'op afroep', ['CursusID', 'Cursusnaam']].reset_index(drop = True)
    count_calls = len(courses_calls)

    for call_idx in range(count_calls):

        geoict_df.loc[count_events+call_idx, 'id'] = courses_calls.loc[call_idx, 'CursusID'] + '_opafroep'

        geoict_df.loc[count_events+call_idx, 'cursusnaam'] = courses_calls.loc[call_idx, 'Cursusnaam']

        geoict_df.loc[count_events+call_idx, 'tekst'] = 'op afroep'

        geoict_df.loc[count_events+call_idx, 'datum'] = '2099-12-31'

    return geoict_df

def create_cursusdatums_website(information_df, planning_df, output_directory, output_filename):
    """
    This function will create the CSV file that can be uploaded to the geo-ict website for the forms (cursusdatums)
    It will make the dataframe and write it to a csv file that can be uploaded in the PHP environment of the website
    """
    geoict_df = create_geoict_df(information_df = information_df, planning_df = planning_df)
    geoict_df.to_csv(os.path.join(output_directory, output_filename), sep = ";", index = False)

def create_product(parent, coursenumber, information_df, website):
    """
    This function will add the products/courses with their basic information to the main root
    """
    for colname in information_df.columns.tolist(): 
        if (information_df.loc[information_df.ID == coursenumber, colname].values[0] != 0): # only add information if it is available (not 0)
            if website == 'edubookers':
                if (colname == 'Name') | (colname == 'Description'): # if it's a name of description, use CDATA instead or a regular string
                    new_product_information = etree.SubElement(parent, 'training_'+colname.lower()) # the nodes need to start with 'training_...' for the Edubookers XML
                    new_product_information.text = etree.CDATA(information_df[information_df.ID == coursenumber][colname].values[0]) 
                elif (colname == 'Additional_costs') | (colname == 'Additional_costs_description'): # additional costs are added seperately
                    continue
                elif (colname == 'ID'): # the course ID is started with COURSE_... , so that it is a correct ID according to XML standards
                    new_product_information = etree.SubElement(parent, 'training_'+colname.lower())
                    new_product_information.text = 'COURSE_'+str(information_df[information_df.ID == coursenumber]['ID'].values[0])
                else:
                    add_product_information(parent = parent, 
                                            coursenumber = coursenumber, 
                                            information_type = colname,
                                            information_df = information_df,
                                            website = website)

            elif (website == 'springest') | (website == 'studytube'):
                if (colname == 'Name') | (colname == 'Description'): # if it's a name of description, use CDATA instead or a regular string
                    new_product_information = etree.SubElement(parent, colname) 
                    new_product_information.text = etree.CDATA(information_df[information_df.ID == coursenumber][colname].values[0]) 
                elif (colname == 'AdditionalCosts') | (colname == 'AdditionalCosts_description'): # additional costs are added seperately
                    continue
                elif (colname == 'ID'): # the course ID is started with COURSE_... , so that it is a correct ID according to XML standards
                    new_product_information = etree.SubElement(parent, colname)
                    new_product_information.text = 'COURSE_'+str(information_df[information_df.ID == coursenumber]['ID'].values[0])
                else:
                    add_product_information(parent = parent, 
                                            coursenumber = coursenumber, 
                                            information_type = colname,
                                            information_df = information_df,
                                            website = website)
            else:
                raise ValueError('dit is geen correcte website, kies uit: springest, studytube of edubookers')

def create_schedules(parent, coursenumber, information_df, planning_df, website):
    """
    This function will create the schedules of the courses to the product/course, according to the format specified by the website
    """
    # Will create the nodes with information about the planning including the schedule with all the coursedays
    duration = information_df.loc[information_df.ID == coursenumber, 'Duration'].values[0] # duration of the course
    startdays = planning_df.loc[(planning_df.ID == coursenumber) & (planning_df.Day == '1'),'RowID'].reset_index(drop=True) # list of all the startdays of that course
    amount_startdays = len(startdays) # amount of startdays of that course

    if website == 'springest':
        for i in range(amount_startdays):
            # Create a new event
            new_event_child = etree.SubElement(parent, 'StartingDatePlace') # create a new node for the new event

            # Creates a df with the information that needs to be added
            event_info = pd.DataFrame({'type': ['ID', 'Startdate', 'Enddate', 'Place', 'StartdateIsMonthOnly', 'EnddateIsMonthOnly', 'StartGuaranteed'],
                                       'value': [str(planning_df.loc[planning_df.RowID == startdays[i], 'EventID'].values[0]),
                                                 str(planning_df.loc[planning_df.RowID == startdays[i], 'Date'].values[0]),
                                                 str(planning_df.loc[planning_df.RowID == str(int(startdays[i]) + int(duration) - 1), 'Date'].values[0]),
                                                 str(planning_df.loc[planning_df.RowID == startdays[i], 'Place'].values[0]),
                                                 'false', 'false', 'false']})

            # Add the information from the event_info df
            add_information_from_df(parent = new_event_child, df = event_info)

            # Add the schedule
            new_schedule = etree.SubElement(new_event_child, 'Schedule') 
            for days in range(int(duration)): 
                # Add a new courseday
                new_courseday = etree.SubElement(new_schedule, 'Courseday') 
                for colname in ['Date', 'Place', 'StartTime', 'EndTime']: # Add the information to that courseday
                    add_courseday_information(parent = new_courseday, 
                                              schedule_information = colname, 
                                              daynumber = days,
                                              planning_df = planning_df,
                                              startday_index = startdays[i])

                # Add the name of the courseday (Cursusdag plus the daynumber)
                name_courseday = etree.Element('Name')
                name_courseday.text = 'Cursusdag ' + str(days+1)
                new_courseday.insert(3, name_courseday)

    elif website == 'studytube':
        for i in range(amount_startdays): 
            # Create a new event (livesession)
            new_event_child = etree.SubElement(parent, 'LiveSession') 

            # Creates a df with the information that needs to be added
            event_info = pd.DataFrame({'type': ['ID', 'LocationName', 'Location', 'LiveSessionClosed'],
                                       'value': ['EVENT_'+str(planning_df.loc[planning_df.RowID == startdays[i], 'EventID'].values[0]),
                                                 'kantoor '+ str(planning_df.loc[planning_df.RowID == startdays[i], 'LocationName'].values[0]),
                                                 str(planning_df.loc[planning_df.RowID == startdays[i], 'LocationName'].values[0]) + ', the Netherlands',
                                                 'false']})
            
            # Add the information from the event_info df
            add_information_from_df(parent = new_event_child, df = event_info)

            # Add the schedule
            new_schedule = etree.SubElement(new_event_child, 'LiveSessionDates') 
            for days in range(int(duration)):
                # Add a new courseday
                new_courseday = etree.SubElement(new_schedule, 'LiveSessionDate') 

                # Creates a df with the schedule information
                schedule_info = pd.DataFrame({'type': ['StartDate', 'StartTime', 'EndTime'],
                                              'value': [str(planning_df.loc[planning_df.RowID == str(int(startdays[i]) + days), 'Date'].values[0]),
                                                        str(planning_df.loc[planning_df.RowID == str(int(startdays[i]) + days), 'StartTime'].values[0]),
                                                        str(planning_df.loc[planning_df.RowID == str(int(startdays[i]) + days), 'EndTime'].values[0])]})
                
                # Add the information from the schedule_info df
                add_information_from_df(parent = new_courseday, df = schedule_info)

    elif website == 'edubookers':
        for i in range(amount_startdays): 
            # Create a new event (training_item)
            new_event_child = etree.SubElement(parent, 'training_item') 

            # Creates a df with the information that needs to be added
            event_info = pd.DataFrame({'type': ['training_item_startassurance', 'training_item_startdate', 'training_item_time_start', 'training_item_time_end'],
                                        'value': ['false', str(planning_df.loc[planning_df.RowID == startdays[i], 'Date'].values[0]),
                                                  str(planning_df.loc[planning_df.RowID == startdays[i], 'Time_start'].values[0]),
                                                  str(planning_df.loc[planning_df.RowID == startdays[i], 'Time_end'].values[0])]})
            
            # Add the information from the event_info df
            add_information_from_df(parent = new_event_child, df = event_info)

            # Add the schedule
            new_schedule = etree.SubElement(new_event_child, 'training_item_followup') # create the Schedule node
            for days in range(1, int(duration)): 
                # Create a df with the schedule information
                schedule_info = pd.DataFrame({'type': ['training_item_followup_date', 'training_item_followup_start', 'training_item_followup_end'],
                                              'value': [str(planning_df.loc[planning_df.RowID == str(int(startdays[i]) + days), 'Date'].values[0]),
                                                        str(planning_df.loc[planning_df.RowID == str(int(startdays[i]) + days), 'Time_start'].values[0]),
                                                        str(planning_df.loc[planning_df.RowID == str(int(startdays[i]) + days), 'Time_end'].values[0])]})
                
                # Add the information from the schedule_info df
                add_information_from_df(parent = new_schedule, df = schedule_info)
                
            # Creates a df with the information that needs to be added (extra)
            event_info = pd.DataFrame({'type': ['training_item_location', 'training_item_price'],
                                        'value': [str(planning_df.loc[planning_df.RowID == startdays[i], 'Location'].values[0]),
                                                  str(information_df.loc[information_df.ID == coursenumber, 'Price'].values[0])]})
            
            # Add the information from the event_info df
            add_information_from_df(parent = new_event_child, df = event_info)

    else:
        raise ValueError('dit is geen correcte website, kies uit: springest, studytube of edubookers')

def add_additional_costs(parent, coursenumber, information_df, website):
    """
    This function will add the additional costs according to the format for the website
    """
    if website == 'springest':
        # Create a df with the information that is needed about the additional costs
        cost_info = pd.DataFrame({'type': ['Type', 'Price', 'VatIncluded', 'VatAmount', 'Mandatory'],
                                  'value': ['study material',str(information_df.loc[information_df.ID == coursenumber, 'AdditionalCosts'].values[0]),
                                            'no', str(int(information_df.loc[information_df.ID == coursenumber, 'AdditionalCosts'].values[0])*0.21), 'true']})
        
        # Add the information from the cost_info df
        add_information_from_df(parent = parent, df = cost_info)

    elif website ==  'studytube':
        # Create a df with the information that is needed about the additional costs
        cost_info = pd.DataFrame({'type': ['Type', 'AdditionalCostPriceExVAT', 'VATPercentage'],
                                  'value': [str(information_df.loc[information_df.ID == coursenumber, 'AdditionalCosts_description'].values[0]),
                                            str(information_df.loc[information_df.ID == coursenumber, 'AdditionalCosts'].values[0]),
                                            '21']})

        # Add the information from the cost_info df
        add_information_from_df(parent = parent, df = cost_info)

    elif website == 'edubookers':
        # Add the additional costs on a specific place in the XML (empty nodes)
        new_additional_costs = etree.Element('training_additional_costs')
        parent.insert(5, new_additional_costs)
        new_additional_costs_description = etree.Element('training_additional_costs_description')
        parent.insert(6, new_additional_costs_description)

        # If there are additional costs, fill in the values and the description
        if information_df.loc[information_df.ID == coursenumber, 'Additional_costs'].values[0] != 0:
            new_additional_costs.text = str(information_df.loc[information_df.ID == coursenumber, 'Additional_costs'].values[0])
            new_additional_costs_description.text = str(information_df.loc[information_df.ID == coursenumber, 'Additional_costs_description'].values[0])
    else:
        raise ValueError('dit is geen correcte website, kies uit: springest, studytube of edubookers')


def write_to_xml(root, output_directory, output_filename):
    """
    This function writes the root with all its added content to an XML file
    """
    created_tree = etree.ElementTree(root)
    created_tree.write(open(os.path.join(output_directory, output_filename), 'wb'),
                       pretty_print=True, 
                       encoding = 'utf-8',
                       xml_declaration = True)

def create_xml_website(information_df, planning_df, output_directory, output_filename, website):
    """
    This function will combine other functions in this script to create the final XML for the website and writes it to the output_directory
    """
    # The creation of the springest and studytube file are quite similar, so there are made in the same way except for a few things studytube does different
    if (website == 'springest') | (website == 'studytube'):
        root = etree.Element('Products') # The main root of the file

        for coursenumber in information_df.loc[:,'ID']:
        # Make a new node for the product
            new_product_node = etree.SubElement(root, 'Product')

            # Create the product: basic information about the course
            create_product(parent = new_product_node,
                           coursenumber = coursenumber,
                           information_df = information_df,
                           website = website)

            # If the product has additional costs, add these with the additional info about these costs
            new_additional_costs = etree.Element('AdditionalCosts')
            new_product_node.insert(8, new_additional_costs)
            if information_df.loc[information_df.ID == coursenumber, 'AdditionalCosts'].values[0] != 0: # if there are any additional costs
                new_additional_cost = etree.SubElement(new_additional_costs, 'AdditionalCost')

                add_additional_costs(parent = new_additional_cost,
                                     coursenumber = coursenumber,
                                     information_df = information_df,
                                     website = website)
            if website == 'studytube':
                new_schedule_type = etree.Element('ScheduleType')

                # Add the node for all events of this course
                new_event = etree.SubElement(new_product_node, 'LiveSessions')  
            else:
                new_event = etree.SubElement(new_product_node, 'StartingDatePlaces')  
           
            if sum(planning_df.ID.isin([coursenumber])) > 0: # if coursenumber is planned
                if website == 'studytube':
                    new_schedule_type.text = 'scheduled'
                
                create_schedules(parent = new_event,
                                 coursenumber = coursenumber,
                                 information_df = information_df,
                                 planning_df = planning_df,
                                 website = website)
            else:
                if website == 'studytube':
                    new_schedule_type.text = 'nodate'
            if website == 'studytube':
                new_product_node.insert(15, new_schedule_type)

                # Add nodes that will be empty, but need to be included in the XML anyway
                empty_nodes = pd.DataFrame({'nodename': ['Agenda', 'EducationalPoints', 'QualityMarks', 'Trainers', 'Discounts', 'RequiredUserFields'],
                                            'index': [3, 9, 10, 12, 20, 21]})
            else:
                empty_nodes = pd.DataFrame({'nodename': ['Images', 'VideoEmbed', 'PriceExemptAmount', 'PriceAgreement', 'PriceInfo', 'Trainers', 'DurationAgreement',
                                                        'Runtime', 'ExtraInstructionsAfterBooking', 'ParticipantsAgreement', 'ContactPerson', 'AllowedSites', 
                                                        'Regions', 'Level', 'CrohoID', 'CreboID', 'PriceDiscounts', 'PePoints', 'Moments', 'CustomLtiParams'],
                                        'index': [3, 4, 9, 11, 14, 15, 19, 20, 22, 24, 27, 29, 30, 31, 32, 33, 34, 35, 36, 38]})

            # Add the actual empty nodes
            for empty in empty_nodes.nodename:
                new_empty_node = etree.Element(empty)
                new_product_node.insert(empty_nodes.loc[empty_nodes.nodename == empty, 'index'].values[0], new_empty_node)

    elif website == 'edubookers':
        root = etree.Element('trainings') 

        for coursenumber in information_df.loc[:,'ID']:
            # Make a new node for the product
            new_product_node = etree.SubElement(root, 'training')

            create_product(parent = new_product_node,
                           coursenumber = coursenumber,
                           information_df = information_df,
                           website = website)

            add_additional_costs(parent = new_product_node,
                                 coursenumber = coursenumber,
                                 information_df = information_df,
                                 website = website)
        
            new_event = etree.SubElement(new_product_node, 'training_items')  # create a new node for all events of this course

            if sum(planning_df.ID.isin([coursenumber])) > 0: # if coursenumber is planned
                create_schedules(parent = new_event,
                                 coursenumber = coursenumber,
                                 information_df = information_df,
                                 planning_df = planning_df,
                                 website = website)
    write_to_xml(root = root,
                 output_directory = output_directory,
                 output_filename = output_filename)

def check_database(information_df, planning_df):
    # Checks the database if the data is correct

    # All columns that are necessary
    necessary_cols_info = ['Cursusnaam', 'CursusID', 'SpringestID', 'Omschrijving', 'Categorie', 'Onderwerp', 
                      'Duur', 'Duur_eenheid', 'Prijs', 'Extra_kosten', 'Omschrijving_extra_kosten', 'URL', 'PDF_URL']
    necessary_cols_planning = ['RowID', 'EventID', 'CursusID', 'Cursusnaam', 'Locatie', 'Dag', 'Datum', 'Begintijd', 'Eindtijd']

    # All columns that are in the database
    course_information_cols = information_df.columns.tolist()
    course_planning_cols = planning_df.columns.tolist()

    if all(elem in course_information_cols for elem in necessary_cols_info): # check if all necessary columns are present in the course information
        for col in necessary_cols_info:
            if (col != 'Extra_kosten') & (col != 'Omschrijving_extra_kosten'): # nog necessary to have additional costs
                if information_df.loc[:,col].isin([0]).any(): # check if there are any empty values (zeros)
                    raise ValueError('Er missen waarden voor deze kolom: ' + col) # if there are zeros, tell in which column
    else:
        missing = list(set(necessary_cols_info) - set(course_information_cols)) # if there are columns missing, tell which ones
        raise ValueError('Er missen kolommen in de cursusinformatie, namelijk: ' + str(missing))


    if all(elem in course_planning_cols for elem in necessary_cols_planning): # check if all necessary columns are present in the planning
        for col in necessary_cols_planning:
            if planning_df.loc[:,col].isin([0]).any(): # check if there any empty values (zeros)
                raise ValueError('Er missen waarden voor deze kolom: ' + col) # if there are zeros, tell in which column
    else:
        missing = list(set(necessary_cols_planning) - set(course_planning_cols)) # if there are columns missing, tell which ones
        raise ValueError('Er missen kolommen in de cursusinformatie, namelijk: ' + str(missing))