# Pipeline Tariff Web-scraping Project

This project obtains pipeline tariffs and their corresponding details from the top 3 Canadian pipline companies; Enbridge, TC Energy and Transmountain. It obtains pipeline data for exports leaving from Canadian provinces to the United States. Information collected include Tariff name, effective data, replaced tariff (if exist) and corresponding URL for the tariff PDF. Recently another feature was implemented to analyze the title page of the tariffs for more information, however this feature is not very stable with some PDF reads resulting in error.

## Technologies and Libraries Used

* Python 3.7
* BeautifulSoup
* CSV reader and writer
* datetime
* PyPDF2
* numpy
* re

## Results

Executing scrape.py will begin the webscrapping. A message displayed in your console will notify the success or any issues from the task. A tariff-data.csv file will be generated with all the tariff information from the three websites compiled into one document saved in the same directory. 

Executing scrape_test.py will begin the analysis of the tariff title pdf file. Initial downloading of the PDF is required along with the name specified within the python code. For now, the information is displayed within console.

## Contribute

This project welcomes contributions especially in the PDF title scraping part of the project (scrape_test.py). If possible, obtaining the chart data would be a plus or if you know how to allow the PDFs to be opened and analyzed remotely from the URL instead of downloading. Please let me know if you have any updates or ideas to make this project better.
