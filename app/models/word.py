from app import db

class Word(db.Model):
    word_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String)
    # date=db.Column(db.String)
    account_uid=db.Column(db.String, db.ForeignKey('account.account_uid'))
    account=db.relationship('Account', back_populates='words')
    
    def to_dict(self):
        dict = {
            "id": self.word_id,
            "description":self.description
        }
        return dict