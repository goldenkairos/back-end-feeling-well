from app import db

class Word(db.Model):
    word_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    description = db.Column(db.String)
    # date=db.Column(db.String)
    user_id=db.Column(db.Integer, db.ForeignKey('user.user_id'))
    user=db.relationship('User', back_populates='words')
    
    def to_dict(self):
        dict = {
            "id": self.word_id,
            "description":self.description
        }
        return dict