from .models import Monument
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import request
from . import db
import requests
import json

URL_API = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
whole_list=["amusement_park", "aquarium", "art_gallery", "bar", "cafe", "casino", "hindu_temple", "church", "museum", "movie_theater",
    "night_club", "park", "restaurant", "synagogue", "tourist_attraction" ] # wiem, że brzydko wygląda ale przynajmniej krótko się pętle wykonują xd
main = Blueprint('main', __name__)


monuments=[]

@main.route('/')
def index():
    return render_template('index.html')


@main.route('/userpage')
@login_required
def userpage():
    return render_template('userpage.html', name=current_user.login)

@main.route('/profile')
@login_required
def userProfile():
    
    from .models import Tags
    
    tag = Tags.query.filter_by(UserID=current_user.id).first()
    print('id of user: ', current_user.id)
    if tag:
        return render_template('profileWithPreferences.html', name=current_user.login, yourtag=tag)
    return render_template('profile.html', name=current_user.login)    
    

@main.route('/fillform')
@login_required
def fillingForm():
    return render_template('fillform.html')

@main.route('/createPreference', methods=['POST'])
@login_required
def createPreferences():

    args = request.form

    from .models import Tags

    newPreference = Tags(UserID = current_user.id)

    whole_list=["amusement_park", "aquarium", "art_gallery", "bar", "cafe", "casino", "hindu_temple", "church", "museum", "movie_theater",
    "night_club", "park", "restaurant", "synagogue", "tourist_attraction" ] # wiem, że brzydko wygląda ale przynajmniej krótko się pętle wykonują xd

    newPreference.setValues(args,whole_list)
   
    db.session.add(newPreference)
    db.session.commit()
    return render_template('userpage.html', name=current_user.login)


@main.route('/searchMonuments')
@login_required
def searchMonuments():
    monuments.clear()
    return render_template('searchMonuments.html', monums=monuments)

def createURL(latitude, longitude, radius):
    real_radius=int(radius)*1000
    return URL_API+'location='+str(latitude)+','+str(longitude)+'&radius='+str(real_radius)+'&'+'key=AIzaSyBMW5H1JlI7plBq755rVkyuwWpdCktoYfk' # trzymanie klucza w source code, dobry plan, ale chuj w to

def checkIfCorrectType(types):
    for element in whole_list:
        for type in types:
            if type == element:
                return True
    return False

def filterForMonuments(data):
    localmonuments=[]
    for i in range(0,len(data['results'])):
        if checkIfCorrectType(data['results'][i]['types']):
            latitude=data['results'][i]['geometry']['location']['lat']
            longitude=data['results'][i]['geometry']['location']['lng']
            name=data['results'][i]['name']
            rating=data['results'][i]['rating']
            types=data['results'][i]['types']
            photo_reference=data['results'][i]['photos'][0]['photo_reference']
            monument=Monument(name,latitude,longitude,types,rating,photo_reference)
            localmonuments.append(monument)
    return localmonuments     

@main.route('/searchMonuments', methods=['POST'])
@login_required
def getMonuments(): 
    latitude=request.form.get('latitude')
    longitude=request.form.get('longitude')
    radius=request.form.get('radius')
    URL_TO_SEND=createURL(latitude,longitude,radius)
    r = requests.get(url = URL_TO_SEND)
    data=r.json()

    monuments=filterForMonuments(data) # filtrowanie danych żeby typów miejsc niepotrzebnych nie było
    for monument in monuments:
        monument.printMonument()
    json_monuments = json.dumps([ob.__dict__ for ob in monuments])
    print(json_monuments)
    return render_template('searchMonuments.html',monums=json_monuments)


