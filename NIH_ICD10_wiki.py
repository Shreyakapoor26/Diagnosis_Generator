import requests
import re
import csv
from bs4 import BeautifulSoup

# Specify the API endpoint and query parameters
endpoint = 'https://clinicaltables.nlm.nih.gov/api/conditions/v3/search'
params = {'terms': '', 'maxList': 10000000000}

# Send a GET request to the API with the query parameters
response = requests.get(endpoint, params=params)

# Parse the JSON response into Python objects
data = response.json()

# Print the first 10 conditions
disease_list = []
for condition in data[3][:100000]:
    # take the string out of the list
    condition = condition[0]
    disease_list.append(condition)

# remove the content in the brackets in the disease name
for i in range(len(disease_list)):
    disease_list[i] = re.sub(r'\([^)]*\)', '', disease_list[i])

# print(disease_list)

# write code to extract symptoms for each disease from the wiki page
dis_symp = {}
for disease in disease_list:
    # Replace spaces with '_' for the Wikipedia page title
    wiki_title = '_'.join(disease.split())
    # Send a GET request to the Wikipedia page for the disease
    response = requests.get(f'https://en.wikipedia.org/wiki/{wiki_title}')
    # Parse the HTML response using Beautiful Soup
    soup = BeautifulSoup(response.content, 'html.parser')
    # Find the infobox table and extract the contents
    info_table = soup.find('table', {'class': 'infobox'})
    if info_table is not None:
        for row in info_table.find_all('tr'):
            data = row.find('th', {'scope': 'row'})
            if data is not None and data.text == 'Symptoms':
                # Extract the symptoms from the infobox
                symptom = row.find('td')
                # Remove unwanted tags and text from the symptom description
                symptom = re.sub(r'\[[^\]]*\]', '', str(symptom))
                symptom = re.sub(r'<[^>]*>', '', symptom)
                symptom = re.sub(r'\([^)]*\)', '', symptom)
                symptom = re.sub(r'\s+', ' ', symptom)
                symptom = symptom.strip()
                # Store the symptoms for the disease in a dictionary
                dis_symp[disease] = symptom
                break

# Create a list of dictionaries to store the disease and symptoms
dis_symp_list = []
for disease, symptoms in dis_symp.items():
    dis_symp_dict = {'disease': disease, 'symptoms': symptoms}
    dis_symp_list.append(dis_symp_dict)

# write dis_symp_single_col to a csv file
with open('disease_symptoms_wiki.csv', 'w', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=['disease', 'symptoms'])
    writer.writeheader()
    for row in dis_symp_list:
        writer.writerow(row)