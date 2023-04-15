from flask import Flask, render_template, request
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
import numpy as np

app = Flask(__name__)

# Load dataset into pandas DataFrame
data = pd.read_csv('combined_data.csv')

# Preprocess data by splitting Symptoms column and cleaning data
data['symptoms'] = data['symptoms'].apply(lambda x: x.split(','))
data['symptoms'] = data['symptoms'].apply(lambda x: [s.strip().lower() for s in x])

# Encode target labels as integers
le = LabelEncoder()
data['disease'] = le.fit_transform(data['disease'])

# Vectorize input features using CountVectorizer
vectorizer = CountVectorizer()
X_vec = vectorizer.fit_transform([' '.join(s) for s in data['symptoms']])

# Train classifier on all data
clf = MultinomialNB()
clf.fit(X_vec, data['disease'])

# Define home page route
@app.route('/')
def home():
    return render_template('index.html')

# Define diagnosis page route
@app.route('/diagnosis', methods=['POST'])
def diagnosis():
    # Take user input of symptoms
    user_input = request.form['symptoms']
    user_symptoms = user_input.split(',')

    # Preprocess user input
    user_symptoms = [s.strip().lower() for s in user_symptoms]

    # Vectorize user input
    user_input_vec = vectorizer.transform([' '.join(user_symptoms)])

    # Predict diseases based on user input
    predicted_probabilities = clf.predict_proba(user_input_vec)
    top_n_indices = np.argsort(predicted_probabilities[0])[::-1][:10] # Top 10 most likely diseases
    top_n_probabilities = predicted_probabilities[0][top_n_indices]

    # Convert predicted labels back to disease names
    predicted_diseases = le.inverse_transform(top_n_indices)

    # Mayo Clinic URL for disease lookup
    mayo_base_url = "https://www.mayoclinic.org/diseases-conditions/"

    # Create list of tuples containing disease name, likelihood, and Mayo Clinic and DBMI URL
    diseases_list = []
    for i, disease in enumerate(predicted_diseases):
        mayo_link = mayo_base_url + disease.lower().replace(" ", "-")
        disease_info = (disease, round(top_n_probabilities[i], 3), mayo_link)
        diseases_list.append(disease_info)

    # Render diagnosis template with list of predicted diseases
    return render_template('diagnosis.html', symptoms=user_symptoms, diseases=diseases_list)

if __name__ == '__main__':
    app.run(debug=True, port=8080)
