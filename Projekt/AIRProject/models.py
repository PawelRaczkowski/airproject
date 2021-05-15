from flask_login import UserMixin
from . import db

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    login = db.Column(db.String(1000), unique=True)
    password = db.Column(db.String(100))

class Tags(db.Model):
    UserID = db.Column(db.Integer, primary_key=True) 
    amusement_park = db.Column(db.Integer)
    aquarium = db.Column(db.Integer)
    art_gallery = db.Column(db.Integer)
    bar = db.Column(db.Integer)
    cafe = db.Column(db.Integer)
    casino = db.Column(db.Integer)
    hindu_temple = db.Column(db.Integer)
    church = db.Column(db.Integer)
    movie_theater = db.Column(db.Integer)
    museum = db.Column(db.Integer)
    night_club = db.Column(db.Integer)
    park = db.Column(db.Integer)
    restaurant = db.Column(db.Integer)
    synagogue = db.Column(db.Integer)
    tourist_attraction = db.Column(db.Integer)

    def setValues(self, args, whole_list):
        for arg in args:
            print(arg)
            self.setValue(arg,10)
            whole_list.remove(arg)
        for arg in whole_list:
            self.setValue(arg,3)
        
    def setValue(self, key, value): # nie wiem czy zadziała :p
        if (key == "amusement_park"): self.amusement_park = value
        elif (key == "aquarium"): self.aquarium = value
        elif (key == "art_gallery"): self.art_gallery = value
        elif (key == "bar"): self.bar = value
        elif (key == "cafe"): self.cafe = value
        elif (key == "casino"): self.casino = value
        elif (key == "hindu_temple"): self.hindu_temple = value
        elif (key == "church"): self.church = value
        elif (key == "movie_theater"): self.movie_theater = value
        elif (key == "museum"): self.museum = value
        elif (key == "night_club"): self.night_club = value
        elif (key == "park"): self.park = value
        elif (key == "restaurant"): self.restaurant = value
        elif (key == "synagogue"): self.synagogue = value
        elif (key == "tourist_attraction"): self.tourist_attraction = value

    def addValue(self, key, value): # nie wiem czy zadziała :p
        if (key == "amusement_park"): self.amusement_park += value
        elif (key == "aquarium"): self.aquarium += value
        elif (key == "art_gallery"): self.art_gallery += value
        elif (key == "bar"): self.bar += value
        elif (key == "cafe"): self.cafe += value
        elif (key == "casino"): self.casino += value
        elif (key == "hindu_temple"): self.hindu_temple += value
        elif (key == "church"): self.church += value
        elif (key == "movie_theater"): self.movie_theater += value
        elif (key == "museum"): self.museum += value
        elif (key == "night_club"): self.night_club += value
        elif (key == "park"): self.park += value
        elif (key == "restaurant"): self.restaurant += value
        elif (key == "synagogue"): self.synagogue += value
        elif (key == "tourist_attraction"): self.tourist_attraction += value

    def remValue(self, key, value): # nie wiem czy zadziała :p
        if (key == "amusement_park"): self.amusement_park -= value
        elif (key == "aquarium"): self.aquarium -= value
        elif (key == "art_gallery"): self.art_gallery -= value
        elif (key == "bar"): self.bar -= value
        elif (key == "cafe"): self.cafe -= value
        elif (key == "casino"): self.casino -= value
        elif (key == "hindu_temple"): self.hindu_temple -= value
        elif (key == "church"): self.church -= value
        elif (key == "movie_theater"): self.movie_theater -= value
        elif (key == "museum"): self.museum -= value
        elif (key == "night_club"): self.night_club -= value
        elif (key == "park"): self.park -= value
        elif (key == "restaurant"): self.restaurant -= value
        elif (key == "synagogue"): self.synagogue -= value
        elif (key == "tourist_attraction"): self.tourist_attraction -= value