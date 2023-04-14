import requests
from bs4 import BeautifulSoup
import csv

url = 'https://people.dbmi.columbia.edu/~friedma/Projects/DiseaseSymptomKB/index.html'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

disease_symptom_dict = {}

# Initialize variables
disease_name = ""
symptoms = []

# Iterate over each table row
for row in soup.find_all('tr')[1:]:
    cells = row.find_all('td')

    # Extract disease name and symptoms
    new_disease_name = cells[0].text.strip()
    new_symptoms = cells[2].text.strip().split(", ")

    # If the current row has a new disease name, save the previous disease name and symptoms
    if new_disease_name:
        if disease_name:
            disease_symptom_dict[disease_name] = symptoms
        disease_name = new_disease_name
        symptoms = new_symptoms
    else:
        # If the current row has no disease name, add the symptoms to the previous disease name
        symptoms += new_symptoms

# Save the last disease name and symptoms
disease_symptom_dict[disease_name] = symptoms

# Create a new dictionary to hold the cleaned disease names and symptoms
cleaned_disease_symptom_dict = {}

# Iterate over each disease and symptoms in the original dictionary
for disease, symptoms in disease_symptom_dict.items():
    # Clean the disease name
    disease = disease.split('_', 1)[-1]
    while '_' in disease:
        disease = disease.split('_', 1)[-1]
    disease = disease.replace('\n', '').replace('  ', ' ')

    # Clean the symptom names
    cleaned_symptoms = []
    for symptom in symptoms:
        while '_' in symptom:
            symptom = symptom.split('_', 1)[-1]
        symptom = symptom.replace('_', '')
        symptom = symptom.replace('\n', '').replace('  ', ' ')
        symptom = [s.strip() for s in symptom.split(",")]
        cleaned_symptoms += symptom

    # Add the cleaned disease and symptoms to the new dictionary
    cleaned_disease_symptom_dict[disease] = ", ".join(cleaned_symptoms)

# Save the disease and symptom data into a csv file
with open('dbmi_disease_symptoms.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['disease', 'symptoms'])
    for disease, symptoms in cleaned_disease_symptom_dict.items():
        writer.writerow([disease, symptoms])
