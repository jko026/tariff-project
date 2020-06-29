import requests
from bs4 import BeautifulSoup
from csv import writer
from datetime import datetime

# urls from enbridge, tcenergy and transmountain with tariff data
url = ['https://www.enbridge.com/Projects-and-Infrastructure/For-Shippers/Tariffs/Enbridge-Bakken-Pipeline-Company-Inc-Bakken-Canada-tariffs.aspx',
'https://www.enbridge.com/Projects-and-Infrastructure/For-Shippers/Tariffs/Enbridge-Pipelines-Inc-Canadian-Mainline-Tariffs.aspx',
'https://www.enbridge.com/Projects-and-Infrastructure/For-Shippers/Tariffs/Enbridge-Pipelines-Inc-Line-8-Tariffs.aspx',
'https://www.enbridge.com/Projects-and-Infrastructure/For-Shippers/Tariffs/Enbridge-Pipelines-Inc-Line-9-Tariffs.aspx',
'https://www.enbridge.com/Projects-and-Infrastructure/For-Shippers/Tariffs/Enbridge-Pipelines-NW-Inc-Norman-Wells-Tariffs.aspx',
'https://www.enbridge.com/Projects-and-Infrastructure/For-Shippers/Tariffs/Enbridge-Southern-Lights-GP-Inc-Southern-Lights-Canada-Tariffs.aspx',
'https://www.enbridge.com/Projects-and-Infrastructure/For-Shippers/Tariffs/Express-Pipeline-Ltd-Express-Canada-Tariffs.aspx',
'https://www.tcenergy.com/operations/oil-and-liquids/keystone-pipeline-system-shipper-info/',
'https://www.transmountain.com/tolls-tariffs']

# csv file writer
with open('tariff-data.csv', 'w') as csv_file:
    csv_writer = writer(csv_file)
    headers =  ['Effective Date','Tariff','PDF','Replace','Old PDF']
    csv_writer.writerow(headers)

    # checks which website each url is from since weblayout is specific and customized to each scrape
    for eachUrl in url:
  
        response = requests.get(eachUrl)
        soup = BeautifulSoup(response.text,'html.parser')

        # scrapes data from embridge website
        if 'enbridge.com' in eachUrl:
            tariffs = soup.find_all(class_='tariff-item')

            for tariff in tariffs:
                description = tariff.select('p')[0].get_text().replace('Description: ','')
                # check description for IJT or local tolls keyword to know it is a tariff we need
                if 'Local Tolls' in description or 'International Joint Rates' in description or 'Toll schedule' in description:
                    tNames = tariff.find_all(class_='tariff-code')
                    title = tNames[0].get_text().replace('\n','').split(' (')[0]
                    replace = tNames[1].get_text().replace('\n','').split(' (')[0]
                    links = tariff.find_all(class_='tariff-header')
                    link = 'https://www.enbridge.com/'+links[0].find('a')['href']
                    oldLink = 'https://www.enbridge.com/'+links[1].find('a')['href']
                    eDate = tariff.select('p')[4].get_text().replace('Effective Date: ','')
                    # attributes obtained and added one by one to csv file
                    csv_writer.writerow([eDate, title, link, replace, oldLink])

            csv_writer.writerow([])
    
        # scrapes data from tcenergy website
        if 'tcenergy.com' in eachUrl:
            tariffs = soup.find_all('a')

            # this website's formatting is odd so data was collected using two keyword searches. counters used to verify all data was collected.
            countByLink = 0
            countByClass = 0
            for atag in tariffs:
                if atag.find(class_='file-name') is not None:
                    # check url for IJT keyword to know if it is a tariff we need
                    if 'ijt' in atag.get('href'):
                        link = 'https://www.tcenergy.com/'+atag.get('href')
                        tariff = atag.find(class_='file-name').get_text()
                        title = tariff.split('International')[0].strip()
                        eDate = tariff.split('effective ')[1].split(')')[0]
                        countByLink = countByLink + 1
                        # attributes obtained and added one by one to csv file
                        csv_writer.writerow([eDate, title, link])
                    # check description for IJT keyword to compare with url to see if all data were obtained.
                    if 'International Joint Rate Tariff' in (atag.find(class_='file-name')).get_text().replace('\n',''):
                        countByClass = countByClass + 1

            # if an error exist, error message is displayed        
            if (countByClass == 0) or (countByClass < countByLink) or (countByClass > countByLink):
                print('An error has been detected. Entries not added.')
                print('There are '+ countByClass +' found entries and '+ countByLink +' found links.')
            
            csv_writer.writerow([])

        # scrapes data from transmountain website
        if 'transmountain.com' in eachUrl:
            tariffs = soup.find_all(class_='table-wrapper')

            # counter to verify all data was collected
            count = 0
            for tariff in tariffs:
                description = tariff.div.table.thead.tr.text
                # check that tariffs are to a port from Canada not a local tariff in another country
                if 'Local Rate' not in description:
                    dataList = tariff.div.tbody.find_all('tr')
                    title = str(dataList[4].get_text()).replace('\n','-').split('-')[2]
                    replace = str(dataList[5].get_text()).replace('\n','-').split('-')[2]
                    link = dataList[4].find('a')['href']
                    oldLink = dataList[5].find('a')['href']
                    date = str(dataList[3].text.replace('\n',' ')).split(' ')[2]
                    eDate = datetime.strptime(date, '%m/%d/%Y').strftime('%B %d, %Y')
                    count = count + 1
                    # attributes obtained and added one by one to csv file
                    csv_writer.writerow([eDate, title, link, replace, oldLink])

            # if an error exist, error message is displayed
            if count == 0:
                print('An error has been detected. Entries not added.')
                print('The issue may be due to a recent change of html formatting. Please review scrape code.')

            csv_writer.writerow([])


print('File successfully exported.')