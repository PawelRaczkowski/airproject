from AIRProject import db

class Tags(db.Model):
    UserID = db.Column(db.Integer, primary_key=True) 
    amusement_park = db.Column(db.Integer)
    amusement_park = db.Column(db.Integer)
    aquarium = db.Column(db.Integer)
    art_gallery = db.Column(db.Integer)
    bar = db.Column(db.Integer)
    cafe = db.Column(db.Integer)
    casino = db.Column(db.Integer)
    hindu_temple = db.Column(db.Integer)
    church = db.Column(db.Integer)
    museum = db.Column(db.Integer)
    movie_theater = db.Column(db.Integer)
    museum = db.Column(db.Integer)
    movie_theater = db.Column(db.Integer)
    night_club = db.Column(db.Integer)
    park = db.Column(db.Integer)
    restaurant = db.Column(db.Integer)
    synagogue = db.Column(db.Integer)
    tourist_attraction = db.Column(db.Integer)