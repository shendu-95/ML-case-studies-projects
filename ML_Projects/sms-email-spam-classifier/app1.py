import streamlit as st
import pickle
import nltk
import string
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer


ps = PorterStemmer()


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():  # removes the special characters
            y.append(i)

    text = y[:]  # cloning
    y.clear()

    for i in text:
        if i not in stopwords.words(
                'english') and i not in string.punctuation:  # filters out the stop words and punctuations
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))  # run the stemming function in this step

    return " ".join(y)



tdidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))



st.title('Message Spam Classifier')

input_message = st.text_area('Enter the message')

if st.button('Predict'):
    # 1. preprocess
    transform_message = transform_text(input_message)
    # 2. vectorize
    vector_input = tdidf.transform([transform_message])
    # 3. predict
    result = model.predict(vector_input)[0]
    # 4. Display
    if result == 1:
        st.header('Message is spam')
    else:
        st.header('Message not spam')


