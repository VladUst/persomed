import os
import pandas as pd


def read_data():
    pre = os.path.dirname(os.path.realpath(__file__))
    fname = 'disease_symptoms.xlsx'
    path = os.path.join(pre, fname)
    data = pd.read_excel(path)
    symptoms_to_indicators = pd.get_dummies(data.Symptom)
    diseases_list = data['Disease']
    df_diseases_symptoms = pd.concat(
        [diseases_list, symptoms_to_indicators], axis=1)
    df_diseases_symptoms.drop_duplicates(keep='first', inplace=True)
    df_diseases_symptoms = df_diseases_symptoms.groupby(
        'Disease', sort=False).sum()
    df_diseases_symptoms = df_diseases_symptoms.reset_index()
    return df_diseases_symptoms
