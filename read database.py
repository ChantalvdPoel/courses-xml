def read_courseinfo_springest():
    import pandas as pd

    course_information = pd.read_excel('D:\Stack\Geo-ICT\Trainingen\Cursussen database V7.xlsx',
                                       sheet_name = 'cursussen',
                                       dtype=str,
                                       usecols = ['CursusID', 'Cursusnaam',
                                                  'Omschrijving', 'Prijs',
                                                  'Extra_kosten', 'Omschrijving_extra_kosten',
                                                  'Duur', 'Duur_eenheid', 
                                                  'URL', 'PDF_URL'])


    course_information_springest = course_information.rename(columns = {'CursusID': 'ID',
                                                                        'Cursusnaam': 'Name',
                                                                        'Omschrijving': 'Description',
                                                                        'Prijs': 'Price',
                                                                        'Extra_kosten': 'AdditionalCosts',
                                                                        'Omschrijving_extra_kosten': 'AdditionalCosts_description',
                                                                        'Duur': 'Duration',
                                                                        'Duur_eenheid': 'Duration_unit',
                                                                        'URL': 'WebAddress',
                                                                        'PDF_URL': 'PdfBrochure'})

    return course_information_springest




