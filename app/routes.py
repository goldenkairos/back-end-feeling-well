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

#GET route for ALL words
@word_bp.route("",methods=["GET"])
def get_all_words():
    words = Word.query.all()
    string_of_words = ""
    for word in words:
        # list_of_cards.append(card.to_dict())
        string_of_words+=word.to_dict()["description"] + " "

    # wc = WordCloud(
    #     background_color = 'white',
    #     height = 400,
    #     width=400,
    #     contour_width=3,colormap='rainbow'
    # )

    # wc.generate(string_of_words)

    #store to file
    # return wc.to_file('wordcloud_output.png')

    return jsonify(string_of_words[:-1]), 200

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
