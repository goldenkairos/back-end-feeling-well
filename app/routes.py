import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS
import sys,os #specific the path to the current directory
os.chdir(sys.path[0]) #using os.changedirectory to the current path

from flask import Blueprint, request, jsonify, make_response, abort, send_file
from app import db
from app.models.word import Word
from app.models.user import User


# example_bp = Blueprint('example_bp', __name__)
word_bp = Blueprint('word',__name__,url_prefix='/words')
user_bp = Blueprint('user',__name__,url_prefix='/users')


def count_words(words):
    list_of_words = []
    output_words = {}
    for word in words:
        list_of_words.append(word.to_dict()["description"])
    for word in list_of_words:
        output_words[word] = output_words.get(word, 0) + 1
    return output_words
    


#GET route for ALL words
@word_bp.route("",methods=["GET"])
def get_all_words():
    words = Word.query.all()
    result = count_words(words)
    return jsonify(result), 200

    # return jsonify(string_of_words[:-1]), 200

    # return send_file('wordcloud_output.png', mimetype='image/png'), 200


#POST route for word
@word_bp.route("",methods=["POST"])
def post_word():
    request_body = request.get_json()
    try:
        new_word = Word(
            description=request_body["description"]
        )
    except:
        return abort(make_response({"details": "Invalid data"}, 400))

    
    db.session.add(new_word)
    db.session.commit()
    return jsonify(new_word.to_dict()),201



