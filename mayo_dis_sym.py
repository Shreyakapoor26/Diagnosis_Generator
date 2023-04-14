#################
# Shreya Kapoor #
#    shkapoor   #
#################

'''
This script scrapes the Mayo Clinic website for a list of diseases and their associated symptoms, 
and then writes the data to a CSV file named 'mayo_disease_data.csv'.
'''



import requests
from bs4 import BeautifulSoup
import csv

base_url = 'https://www.mayoclinic.org'

letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
           'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

disease_data = []

for letter in letters:
    url = base_url + '/diseases-conditions/index?letter=' + letter
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    index_div = soup.find('div', {'id': 'index'})
    if index_div is not None:
        ol = index_div.find('ol')
        if ol is not None:
            disease_list = ol.find_all('a')
            for disease in disease_list:
                disease_url = base_url + disease['href']
                disease_response = requests.get(disease_url)
                disease_soup = BeautifulSoup(disease_response.content, 'html.parser')
                symptoms_heading = disease_soup.find('h2', text='Symptoms')
                if symptoms_heading is not None:
                    symptoms_list = symptoms_heading.find_next('ul')
                    if symptoms_list is not None:
                        symptoms = [symptom.text.strip() for symptom in symptoms_list.find_all('li')]
                        disease_data.append([disease.text.strip(), ', '.join(symptoms)])

with open('mayo_disease_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['disease', 'symptoms'])
    writer.writerows(disease_data)
    
print('CSV file generated successfully.')
