from AIRProject import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))