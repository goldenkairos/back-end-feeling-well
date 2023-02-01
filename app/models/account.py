from app import db

class Account(db.Model):
    account_id=db.Column(db.Integer, autoincrement=True)
    account_uid=db.Column(db.String, primary_key=True)
    # email=db.Column(db.String)
    # password=db.Column(db.String)
    words = db.relationship('Word', back_populates='account', lazy=True)
    
    def to_dict_relationship(self):
        return {
            "id":self.account_id,
            "account_uid":self.account_uid,
            # "email":self.email,
            # "password":self.password,
            "words":self.get_words_list()
        }
        
    def to_dict(self):
        return {
            "id":self.account_id,
            "account_uid":self.account_uid
        }
    
    def get_words_string(self):
        string_of_words = ""
        for word in self.words:
            # list_of_cards.append(card.to_dict())
            string_of_words+=word.to_dict().description +" "
        return string_of_words[:-1]