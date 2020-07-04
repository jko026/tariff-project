'''
***** NOT FULLY FUNCTIONAL *****
1) Works with some PDFs, issue occurs when first page of PDF can't be found even though it exist.
   Example: CER 471 or CER 108 or CER 473
2) Currently reads individual PDF locally, ideally get it to remotely read off URL
3) Due to complexity of tables in PDF, retrieving table data can not be done properly
'''

import PyPDF2 as p2
import re
import numpy

# tried to import remotely from web, not working, have not found a way
'''
import urllib.request
from io import BytesIO
url = 'https://www.enbridge.com//~/media/Enb/Documents/Tariffs/2020/CDMN CER 470.pdf'
'''

# get rid of extra spaces when converting from pdf format to string, replace spaces with \n
def replace(string, char):
    pattern = char + '{2,}'
    string = re.sub(pattern, '\n', string)
    return string

# open and read pdf
pdf_file = open('./pdf-files/CER 470.pdf','rb')
read_pdf = p2.PdfFileReader(pdf_file)

# read the title page and format it better for patterns identification
main_page = read_pdf.getPage(0)
main_page_text = main_page.extractText().replace('\n','')
main_page_text = replace(main_page_text, ' ').lower()
if '\nto\n' in main_page_text:
    main_page_text = main_page_text.replace('\nto\n','-to-')
elif '\nto ' in main_page_text:
    main_page_text = main_page_text.replace('\nto ','-to-')
else:
    main_page_text = main_page_text.replace('to ','-to-')

# obtains tariff info, pipeline company, export to and from, tariff effective date
page_list = main_page_text.split('\n')
while('' in page_list):
    page_list.remove('')
tariff_no = page_list[0].strip()
tariff_cancel = main_page_text.split('cancels ')[1].split('\n')[0].strip()
page_in_list_format = main_page_text.lower().split('\n')
tariff_from = (main_page_text.split('from')[1]).split('-to-')[0].strip()
tariff_to = main_page_text.split('-to-')[1].split('\n')[0]
tariff_eDate = main_page_text.split('effective: ')[1].split('\n')[0].strip()

# check to see if tariff is exporting out of canada (wanted tariff)
keyword = ['international','state','alabama','alaska','arizona','arkansas','california','colorado','connecticut','delaware','florida','georgia','idaho','illinois','indiana',
'lowa','kansas','kentucky','louisiana','maine','maryland','massachusetts','michigan','minnesota','mississippi','missouri','montana','nebraska','nevada','new jersey','new mexico',
'new york','carolina','dakota','ohio','oklahoma','oregon','pennsylvania','tennessee','texas','utah','vermont','virginia','washington','wisconsin','wyoming']

tariff_wanted = False
for word in keyword:
    if word in tariff_to.lower():
        tariff_wanted = True

# identify the name of the pipeline
found = False
for item in page_in_list_format:
    if 'pipeline' in item:
        if 'toledo' in item:
            pipeline = 'Enbridge Toledo'
            found = True
        elif 'flanagan' in item:
            pipeline = 'Enbridge/Flanagan South'
            found = True
        elif 'express' in item:
            pipeline = 'Express'
            found = True
        elif 'keystone' in item:
            pipeline = 'Keystone'
            found = True
        elif 'transmountain' in item:
            pipeline = 'Transmountain'
            found = True
        else:
            pipeline = 'Enbridge'
    if found == True:
        break
        

#print information scrapped from titlepage
print('Tariff: '+ tariff_no)
print('Tariff Replace: '+ tariff_cancel)
print('Pipeline: '+ pipeline)
print('Tariff from: '+ tariff_from)
print('Tariff to: '+ tariff_to)
print('Effective: '+ tariff_eDate.capitalize())
print('Export to US: '+ str(tariff_wanted))



# tried to obtain tables in the pdf but due to table complexity, not working
'''
table_page = read_pdf.getPage(2)
print(table_page.extractText().encode('utf-8'))
table_list = table_page.extractText().split('\n')
l = numpy.array_split(table_list,len(table_list)/9)
for i in range(0,10):
    print(l[i])
    '''