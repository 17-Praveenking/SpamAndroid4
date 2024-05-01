from flask import Flask, request, jsonify
import pickle
import string
from nltk.corpus import stopwords
import nltk

from nltk.stem.porter import PorterStemmer


ps = PorterStemmer()


def transform_text(text):
    text = text.lower()
    text = nltk.word_tokenize(text)

    y = []
    for i in text:
        if i.isalnum():
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        if i not in stopwords.words('english') and i not in string.punctuation:
            y.append(i)

    text = y[:]
    y.clear()

    for i in text:
        y.append(ps.stem(i))

    return " ".join(y)


tfidf = pickle.load(open('vectorizer.pkl', 'rb'))
model = pickle.load(open('model.pkl', 'rb'))

main = Flask(__name__)


@main.route('/', methods=['POST'])
def home():
    input_text = request.form.get('input_text')

    transformed_text = transform_text(input_text)

    vector_input = tfidf.transform([transformed_text])

    result = model.predict(vector_input)[0]

    if result == 1:
        return jsonify({'SPAM': str(result)})
    else:
        return jsonify({'HAM': str(result)})


# @main.route('/predict', methods=['POST'])
# def predict():
#     input_text = request.form.get('input_text')

#     transformed_text = transform_text(input_text)

#     vector_input = tfidf.transform([transformed_text])

#     result = model.predict(vector_input)[0]

#     if result == 1:
#         return jsonify({'SPAM': str(result)})
#     else:
#         return jsonify({'HAM': str(result)})

    # result = {'input_text': input_text}
    # return jsonify(result)






#if st.button("Predict"):

  #  transformed_text = transform_text(input_sms)

  #  vector_input = tfidf.transform([transformed_text])

 #   result = model.predict(vector_input)[0]

 #   if result == 1:
  #      st.header("SPAM")
  #  else:
  #      st.header("HAM")
