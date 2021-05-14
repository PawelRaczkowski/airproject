from AIRProject import db

class History(db.Model):
    Id = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer)
    PlaceID = db.Column(db.String(100)) 
    timestamp = db.Column(db.Date)