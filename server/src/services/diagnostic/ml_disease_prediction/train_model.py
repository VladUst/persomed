import pickle
from sklearn.naive_bayes import MultinomialNB
import read_data
import os
from read_data import read_data


def train_model():
    df_diseases_symptoms = read_data()
    x = df_diseases_symptoms[df_diseases_symptoms.columns[1:]]
    y = df_diseases_symptoms['Disease']
    model = MultinomialNB(alpha=0.3)
    model = model.fit(x, y)
    print(model.score(x, y))
    pre = os.path.dirname(os.path.realpath(__file__))
    saved_model = 'prediction_model.sav'
    path = os.path.join(pre, saved_model)
    pickle.dump(model, open(path, 'wb'))


train_model()
