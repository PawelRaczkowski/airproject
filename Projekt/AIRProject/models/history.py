from AIRProject import db

class History(db.Model):
    UserId = db.Column(db.Integer, primary_key=True)
    PlaceID = db.Column(db.Integer) 
    timestamp = db.Column(db.Date)