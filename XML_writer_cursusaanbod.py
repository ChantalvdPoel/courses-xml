# Import all necessary modules
from lxml import etree # lxml is being used instead of ElementTree because lxml can use CDATA which is necessary for this particular XML file
import sys 
import pandas as pd

# Main root of the XML file. All courses will be a node of this root.
root = etree.Element('Products')

# Pandas dataframe with some testdata of basic information about the courses
testdata = pd.DataFrame({   'ID': [487622, 487617], 
                            'Description': ['Dit is de eerste cursus', 'Dit is de tweede cursus'],
                            'Name': ['AutoCAD 2D Basis', 'ArcGIS 2D Basis'],
                            'Price': [795, 995]})

def create_basic_information(new_product_root, coursenumber_local, information):
    # Will create nodes with some basic information for each course: ID, Description, Name & Price
    new_product_information = etree.SubElement(new_product_root, information) # create the new node
    new_product_information.text = str(testdata.loc[coursenumber_local, information]) # fill the node with the appropiate data

def create_product(coursenumber_local):
    # Will add all the courses to the Products root as new nodes
    # Makes use of the create_basic_information function to provide all the basic information for every course
    new_product_root = etree.SubElement(root, 'Product')

    for rowname in testdata.columns.tolist(): # for every column in the table with basic information, do this function
        create_basic_information(new_product_root = new_product_root, 
                                 coursenumber_local = coursenumber_local, 
                                 information = rowname)

# For every course in the database, create a new node with all the basic information
for course in range(0, testdata.shape[0]):
    create_product(course)

# Make a tree of the main root with all its nodes and show it in the pretty XML style
created_tree = etree.ElementTree(root)
created_tree.write(sys.stdout, pretty_print=True)
