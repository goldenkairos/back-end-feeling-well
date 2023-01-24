from app import db

class User(db.Model):
    user_id=db.Column(db.Integer, primary_key=True, autoincrement=True)
    email=db.Column(db.String)
    password=db.Column(db.String)
    words = db.relationship('Word', back_populates='user', lazy=True)
    
    def to_dict(self):
        return {
            "id":self.user_id,
            "email":self.email,
            "password":self.password,
            "words":self.get_words_list()
        }
    
    def get_words_string(self):
        string_of_words = ""
        for word in self.words:
            # list_of_cards.append(card.to_dict())
            string_of_words+=word.to_dict().description +" "
        return string_of_words[:-1]