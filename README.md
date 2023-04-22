# Demo Video: 

## README
This README file provides instructions on how to run the code, how to obtain any required API keys, and a brief description of the program's functionality. The required Python packages for the code to run are also listed.

## Requirements
To run the program, the following Python packages are required:

requests
BeautifulSoup
pandas
numpy
csv
re
scikit-learn
Flask

## SEQUENCE
Run these files in sequence:
1. dbmi_columbia.py 
2. mayo_dis_sym.py
3. NIH_ICD10_wiki.py 
4. merge.py
5. Create a folder name templates and store index.html and diagnosis.html in that folder
6. run app.py

## Data Sources
The data used in the program was obtained from the following sources:
- Mayo Clinic Diseases and Conditions website (https://www.mayoclinic.org/diseases-conditions)
- UMLS disease and symptom table from dbmi.columbia.edu (https://www.dbmi.columbia.edu/our-team/meet-our-faculty/lucila-ohno-machado/)
- NIH API to access ICD-10 disease names and web-parsing of each disease name's symptoms from Wikipedia (https://www.nlm.nih.gov/)

The data was accessed using the Python requests module and the BeautifulSoup library.
The data file is in CSV format and contains information about various medical conditions and their corresponding symptoms. Each row represents a different medical condition, and the first column lists the name of the medical condition while the second column lists its associated symptoms, separated by a comma.

## Data Structure
The program uses CountVectorizer to convert the input symptoms into vectors and the Multinomial Naive Bayes algorithm to classify the disease based on the input symptoms.

## Interaction and Presentation Options
The program has a user-friendly interface that prompts users to input their symptoms. The program then uses the processed data to generate a list of possible diagnoses, ranked by probability. Users can interact with the program to select the most relevant diagnosis or add more symptoms to refine the list. Flask and HTML were used to create the user interface. To use the program, the user must run the Python file and navigate to the provided URL in a web browser. The program's functionality is then available through the user interface.
