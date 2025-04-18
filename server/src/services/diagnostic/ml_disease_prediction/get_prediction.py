import numpy as np
import pickle
import os
from .read_data import read_data
from sklearn.metrics import accuracy_score, f1_score


def get_prediction(symptoms):
    df_diseases_symptoms = read_data()
    pre = os.path.dirname(os.path.realpath(__file__))
    saved_model = 'prediction_model.sav'
    path = os.path.join(pre, saved_model)
    model = pickle.load(open(path, 'rb'))
    all_symptoms = df_diseases_symptoms.columns[1:].values
    test_input = [0] * len(all_symptoms)
    user_symptoms = symptoms
    for symptom in user_symptoms:
        symptom_indices = np.where(all_symptoms == symptom)[0]
        if len(symptom_indices) > 0:
            test_input[symptom_indices[0]] = 1
    
    # Get probabilities for all diseases
    probabilities = model.predict_proba([test_input])[0]
    
    # Get top 3 disease indices
    top_indices = probabilities.argsort()[-3:][::-1]
    
    # Get disease names for top indices
    top_diseases = []
    for idx in top_indices:
        if probabilities[idx] > 0:  # Only include diseases with non-zero probability
            top_diseases.append(model.classes_[idx])
    
    # Limit to at most 3 diseases
    return top_diseases[:3]


def get_model_info():
    """Return information about the model with real metrics calculated using sklearn"""
    # Load the model and training data
    df_diseases_symptoms = read_data()
    pre = os.path.dirname(os.path.realpath(__file__))
    saved_model = 'prediction_model.sav'
    path = os.path.join(pre, saved_model)
    model = pickle.load(open(path, 'rb'))
    
    # Prepare data for evaluation
    X = df_diseases_symptoms[df_diseases_symptoms.columns[1:]].values
    y = df_diseases_symptoms['Disease'].values
    
    # Get predictions
    y_pred = model.predict(X)
    
    # Calculate metrics
    accuracy = accuracy_score(y, y_pred)
    # For multi-class classification, we use weighted average
    f_measure = f1_score(y, y_pred, average='weighted')
    
    return f"Модель диагностики заболеваний по перечню симптомов. Модель имеет точность: {accuracy:.4f}, f-меру: {f_measure:.4f}"
