from flask import Flask, render_template, request
import requests
import random

app = Flask(__name__)

# Define the function to get a random word from the RandomWordAPI
def get_random_word():
    url = "https://random-word-api.herokuapp.com/word?number=1"
    response = requests.get(url)
    word_data = response.json()
    return word_data[0]

# Define the function to get the definition of a word using Free Dictionary API
def get_word_definition(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        definitions = data[0]['meanings'][0]['definitions']
        if definitions:
            return definitions[0]['definition']
        else:
            return "Definition not found."
    else:
        return f"Error: {response.status_code} - {response.text}"

@app.route('/', methods=['GET', 'POST'])
def word_quiz():
    known_words = request.form.getlist('known_words[]', type=str)
    word = get_random_word()
    definition = ""

    if request.method == 'POST':
        if 'know' in request.form:
            known_words.append(word)
        elif 'no' in request.form:
            definition = get_word_definition(word)
        return render_template('index.html', word=word, known_words=known_words, definition=definition)

    return render_template('index.html', word=word, known_words=known_words, definition=definition)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=True)
