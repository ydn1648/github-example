from bs4 import BeautifulSoup
import requests
import pandas as pd
source = requests.get('https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M').text
soup = BeautifulSoup(source, 'lxml')
table = soup.find('table', class_="wikitable sortable")
datalist = table.find_all('td')
df = pd.DataFrame()
x=0
while True:
    PostalCode = datalist[3*x].text
    Borough = datalist[3*x+1].text
    Neighborhood = datalist[3*x+2].text
    Neighborhood = Neighborhood.strip('\n')
    df = df.append(pd.DataFrame({'Postal Code': PostalCode, 'Borough': Borough, 'Neighborhood': Neighborhood}, index = [0]), ignore_index = True)
    if x == ((864-3)/3):
        break
    x+=1
df = df[df['Borough'] != 'Not assigned']
for index, row in df.iterrows():
    if row['Neighborhood'] == 'Not assigned':
        row['Neighborhood'] = row['Borough']
df['Neighborhood'] = df['Neighborhood'].apply(lambda x:x+',')
df_group = df.groupby(by=['Postal Code', 'Borough']).sum()
df_geo = pd.DataFrame()
df_geo = pd.read_csv('Geospatial_Coordinates.csv')
df_gp = df_group.merge(df_geo, how='left', on=['Postal Code'])
df_gp
