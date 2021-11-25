"""
    @script-author : Akhil Matthews
    @script-description : Scraping data of 380 NGOs in Delhi
    @python-version : python 3.9.x
"""

import requests # For reading the html code of the sites
from bs4 import BeautifulSoup # Scraping the data
import pandas as pd # To save data in a csv file

# List of URLs of 38 pages of NGOs in Delhi
urls = []
for page_no in range(723,761):
    urls.append(f'https://ngodarpan.gov.in/index.php/home/statewise_ngo/9705/7/{page_no}')

# Headers for the pandas dataframe
site_html = requests.get(urls[0]).text
soup = BeautifulSoup(site_html, 'html.parser')
table = soup.find('div', class_ = 'ibox-content')
df = {i:[] for i in table.thead.text.split('\n') if len(i)!=0}

table_dict = {}
# Scraping data from the URLs
for url in urls:
    site_html = requests.get(url).text
    soup = BeautifulSoup(markup = site_html, features = 'lxml')
    table = soup.find('div', class_='ibox-content')
    # Get list of rows of data in a page
    rows = table.tbody.find_all('tr')
    for index, row in enumerate(rows):
        # List of values in each cell
        cells = row.find_all('td')
        # Dictionary of index and list of row values
        table_dict[index] = cells

    # Appending to  dictionary
    for row in table_dict.values():
        df['Sr No.'].append(row[0].text)
        df['Name of VO/NGO'].append(str(row[1].text).title())
        df['Registration No.,City & State'].append(str(row[2].text).title()) 
        df['Address'].append(str(row[3].text).title())
        df['Sectors working in'].append(str(row[4].text).title())
df = pd.DataFrame(df)

# Saving data to csv file
df = df.drop('Sr No.', axis = 1)
df.to_csv('data.csv', index = False)
