from flask import Blueprint, request, jsonify, make_response, abort
from app import db
from app.models.word import Word
from app.models.account import Account


# example_bp = Blueprint('example_bp', __name__)
word_bp = Blueprint('word',__name__,url_prefix='/words')
account_bp = Blueprint('account',__name__,url_prefix='/accounts')


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


def validate_account(account_uid):
    chosen_account = Account.query.get(account_uid)
    if chosen_account is None:
        return abort(make_response({"msg":f"Could not find account with id: {account_uid}"}, 404))
    return chosen_account



#GET route for ALL words for ALL users counting words
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

#GET route for All words with account_uid
@word_bp.route("/words-accounts",methods=["GET"])
def get_all_words_accounts():
    words = Word.query.all()
    result = []
    for word in words:
        result.append(word.words_uid_to_dict())
    return jsonify(result), 200

#GET route for ALL words with no account_uid
@word_bp.route("/no_uid_all_words",methods=["GET"])
def get_all_words_no_uid():
    words = Word.query.filter(Word.account_uid==None).all()
    result = []
    for word in words:
        result.append(word.words_uid_to_dict())
    return jsonify(result), 200

#GET route for ALL words for non user counting words
#http://127.0.0.1:5000/words
@word_bp.route("/all_words_non_user",methods=["GET"])
def get_all_words_non_user():
    words = Word.query.filter(Word.account_uid==None).all()
    result = count_words(words)
    return jsonify(result), 200


# DELETE route for ALL words with no userID
@word_bp.route("/no_uid_all_words",methods=['DELETE'])
def delete_all_words_no_uid():
    all_words = Word.query.filter(Word.account_uid==None).all()
    
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
    return jsonify(new_account.to_dict()),201


#GET route for All accounts
#http://127.0.0.1:5000/accounts
@account_bp.route("",methods=["GET"])
def get_all_accounts():
    accounts = Account.query.all()
    result = []
    for account in accounts:
        result.append(account.to_dict_relationship())
    return jsonify(result), 200


#POST A word into One Account
@account_bp.route("/<account_uid>/words", methods=["POST"])
def create_one_word_in_account(account_uid):
    account=validate_account(account_uid)
    request_body = request.get_json()
    try:
        new_word = Word(
            description=request_body["description"]
        )
    except:
        return abort(make_response({"details": "Invalid data"}, 400))
    
    new_word.account_uid = account.account_uid
    # account.words.append(new_word.to_dict()["description"])

    db.session.add(new_word)
    db.session.commit()
   
    return jsonify({"words": new_word.to_dict()}),201

#GET route for All words for One Account uid
@account_bp.route("/<account_uid>/all_words", methods=["GET"])
def get_all_words_in_a_account(account_uid):
    account=validate_account(account_uid)
    result = account.to_dict_relationship()
    words_list = result["words"]
    output_words = {}
    for word in words_list:
        output_words[word] = output_words.get(word, 0) + 1
    return jsonify(output_words), 200


# DELETE route for one word in One Account
#sample route: http://127.0.0.1:5000/words/Excited
@account_bp.route("/<account_uid>/<description>",methods=["DELETE"])
def delete_one_word_in_an_account(account_uid, description):
    # chosen_word = validate_word(description)
    chosen_account = validate_account(account_uid)
    for word in chosen_account.words:
        if word.description == description:

    # chosen_words = Word.query.filter(Word.description==description).all()
    
    # for word in chosen_words:        
            db.session.delete(word)        
            db.session.commit()
        
    return jsonify({"Details":f'{description} successully deleted'}), 200

#DELETE route for ALL words in One Account
@account_bp.route("/<account_uid>/all_words",methods=['DELETE'])
def delete_all_words_in_an_account(account_uid):
    chosen_account = validate_account(account_uid)
    for word in chosen_account.words:
        db.session.delete(word)
        db.session.commit()
    
    return jsonify({"Details":f'All words have been successully deleted'}), 200

#### hello






