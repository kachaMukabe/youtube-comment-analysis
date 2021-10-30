from flask import abort, Flask, jsonify, request, render_template, render_template_string
from flair.models import TextClassifier
from flair.data import Sentence
from textblob import TextBlob

import os
import contractions
import emoji
import re

import googleapiclient.discovery

app = Flask(__name__)

classifier = TextClassifier.load('en-sentiment')

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")


@app.route('/search', methods=['POST'])
def search():
    if not request.form or not 'video' in request.form:
        abort(400)
    url = request.form['video']
    if 'csv' in request.form:
        download_csv = request.form['csv']
        print(download_csv)
    no_of_comments = request.form['no_comments']
    no_of_comments = no_of_comments.split(' ')[0]
    print(no_of_comments )
    video_id = url.split('v=')[1]
    comments = get_comments(video_id, max_results=int(no_of_comments))
    cleaned_comments = clean_comments(comments)
    predictions = list()
    for comment in cleaned_comments:
        if comment == '':
            continue
        sentence = Sentence(comment)
        classifier.predict(sentence)
        label = sentence.labels[0]
        predictions.append({"result": label.value, "polarity": label.score, "comment": comment})

    templ = """
    <table class="table">
        <thead>
            <tr>
                <th>Sentiment</th>
                <th>Polarity</th>
                <th>Comment</th>
            </tr>
        </thead>
        <tbody>
            {% for pred in predictions %}
            <tr>
                <td>{{ pred.result }}</td>
                <td>{{ pred.polarity }}</td>
                <td>{{ pred.comment }}</td>
            </tr>
            {% endfor%}
        </tbody>
    </table>
    """

    return render_template_string(templ, predictions=predictions)


@app.route('/api/v1/analyzeComments', methods=['POST'])
def analyze_comments():
    if not request.json or not 'video' in request.json:
        abort(400)
    print(request.json)
    url = request.json['video']
    video_id = url.split('v=')[1]
    comments = get_comments(video_id)
    cleaned_comments = clean_comments(comments)
    print(cleaned_comments)
    predictions = list()
    for comment in cleaned_comments:
        if comment == '':
            continue
        sentence = Sentence(comment)
        classifier.predict(sentence)
        label = sentence.labels[0]
        predictions.append({"result": label.value, "polarity": label.score, "comment": comment})


    response = {'predictions': predictions}

    return jsonify(response), 200


def get_comments(video_id, max_results=10):
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    DEVELOPER_KEY = os.environ["DEVELOPER_KEY"]

    youtube = googleapiclient.discovery.build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

    request = youtube.commentThreads().list(
            part="snippet,replies", 
            maxResults=max_results,
            videoId=video_id
            )

    response = request.execute()

    comments = response["items"]
    return comments

def clean_comments(comments):
    cleaned_comments = list()
    for comment in comments:
        text = comment["snippet"]["topLevelComment"]["snippet"]["textOriginal"]
        text = remove_emojis(text)
        text = remove_urls(text)
        text = spell_check(text)
        text = expand_contractions(text)
        cleaned_comments.append(text)
    return cleaned_comments

def remove_emojis(text):
    return ''.join(c for c in text if c not in emoji.UNICODE_EMOJI['en'])

def remove_urls(text):
    txt = re.sub("http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+", '', text, flags=re.MULTILINE)
    return txt

def spell_check(text):
    corrected_text = TextBlob(text)
    return str(corrected_text.correct())

def expand_contractions(text):
    return contractions.fix(text)

def remove_stop_words(text):
    pass

if __name__ == "__main__":
    app.run()
