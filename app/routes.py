from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.word import Word
from app.models.account import Account


# example_bp = Blueprint('example_bp', __name__)
word_bp = Blueprint('word',__name__,url_prefix='/words')
account_bp = Blueprint('user',__name__,url_prefix='/users')


def count_words(words):
    list_of_words = []
    output_words = {}
    for word in words:
        list_of_words.append(word.to_dict()["description"])
    for word in list_of_words:
        output_words[word] = output_words.get(word, 0) + 1
    return output_words
    
def validate_word(description):
    chosen_word = Word.query.get(description)
    if chosen_word is None:
        return abort(make_response({"msg": f"Could not find word: {description}"}, 404))
    return chosen_word

#GET route for ALL words for ALL users
#http://127.0.0.1:5000/words
@word_bp.route("",methods=["GET"])
def get_all_words():
    words = Word.query.all()
    result = count_words(words)
    return jsonify(result), 200


#POST route for word for any user
#http://127.0.0.1:5000/words
#in Postman {"description":"any word here"}
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


# DELETE route for one word
#sample route: http://127.0.0.1:5000/words/Excited
@word_bp.route("/<description>",methods=["DELETE"])
def delete_one_word(description):
    # chosen_word = validate_word(description)
    chosen_words = Word.query.filter(Word.description==description).all()
    
    for word in chosen_words:        
        db.session.delete(word)        
        db.session.commit()
        
    return jsonify({"Details":f'{description} successully deleted'}), 200

#DELETE route for ALL words
@word_bp.route("/all",methods=['DELETE'])
def delete_all_words():
    all_words = Word.query.all()
    
    for word in all_words:
        db.session.delete(word)
        db.session.commit()
    
    return jsonify({"Details":f'All words have been successully deleted'}), 200

#POST route for new account
@account_bp.route("",methods=['POST'])
def create_one_user():
    request_body = request.get_json()
    try:
        new_account=Account(
            account_uid=request_body["account_uid"]            
        )
    except:
        return abort(make_response({"details": "Invalid data"}, 400))
    db.session.add(new_account)
    db.session.commit()
    return jsonify({"account":new_account.to_dict()}),201


