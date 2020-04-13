import pandas as pd
import numpy as np

from urllib.request import urlopen
from bs4 import BeautifulSoup


def getHTMLContent(link):
    html = urlopen(link)
    soup = BeautifulSoup(html, 'html.parser')
    return soup


def getTables(url):
    content = getHTMLContent(url)
    tables = content.find_all('table')

    for table in tables:
        print(table.prettify())

def getWIKITable(url):
    content = getHTMLContent(url)
    table = content.find('table', {'class':'wikitable'})
    rows = table.find_all('tr')

    data_columns = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 1:
            data_cells = [cell.text.strip('\n') for cell in cells]
            data_columns.append(data_cells)

    # Get a Dataframe out of data_columns.
    df = pd.DataFrame(data_columns)

    #Get the headers from <th> </th> from row[0] <-- first row.
    headers = rows[0].find_all('th')
    headers = [header.text.strip('\n') for header in headers]

    df.columns = headers
    #print(df)

    ## Now clean/slice the dataframe.
    df['Neighborhood'] = df['Neighborhood'].str.replace(' /', ',')
    clean_df = df.loc[df['Borough'] != 'Not assigned', :]
    clean_df.reset_index(drop=True,inplace=True)
    #print(clean_df)
    #print(clean_df.shape)

    df2 = pd.read_csv(coordinates_file)
    join_df = clean_df.join(df2.set_index('Postal Code'), on='Postal code')

    print(join_df) 
    #print(clean_df.shape)

if __name__ == '__main__':
    url = 'https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'
    coordinates_file = './Geospatial_data.csv'
    #getTables(url)
    df = getWIKITable(url)
