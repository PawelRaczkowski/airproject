from .models import History, Monument, Tags
from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import request
from . import db
import requests
import json
from sqlalchemy import func
from . import cache
from .placeInfo import *

URL_API = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?"
whole_list=["amusement_park", "aquarium", "art_gallery", "bar", "cafe", "casino", "hindu_temple", "church", "museum", "movie_theater",
    "night_club", "park", "restaurant", "synagogue", "tourist_attraction", "point_of_interest", "establishment" ] # wiem, że brzydko wygląda ale przynajmniej krótko się pętle wykonują xd
main = Blueprint('main', __name__)


monuments=[]
sourceLatitude=0
sourceLongitude=0

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
    "night_club", "park", "restaurant", "synagogue", "tourist_attraction", "point_of_interest", "establishment"  ] # wiem, że brzydko wygląda ale przynajmniej krótko się pętle wykonują xd

    newPreference.setValues(args,whole_list)
   
    db.session.add(newPreference)
    db.session.commit()
    return render_template('userpage.html', name=current_user.login)


@main.route('/searchMonuments')
@login_required
def searchMonuments():
    cache.clear()
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
            print(name)
            rating=0
            try:
                rating=data['results'][i]['rating']
            except:
                print('No rating...')
            types=data['results'][i]['types']
            photo_reference=None
            try:
                photo_reference=data['results'][i]['photos'][0]['photo_reference']
            except:
                print("no photo reference")
            monument=Monument(name,latitude,longitude,types,rating,photo_reference)
            localmonuments.append(monument)
    return localmonuments 
    
def GetValueOfType(type, setOfTags):
    if (type == "amusement_park"): return setOfTags.amusement_park
    elif (type == "aquarium"): return setOfTags.aquarium
    elif (type == "art_gallery"): return setOfTags.art_gallery
    elif (type == "bar"): return setOfTags.bar
    elif (type == "cafe"): return setOfTags.cafe
    elif (type == "casino"): return setOfTags.casino
    elif (type == "hindu_temple"): return setOfTags.hindu_temple
    elif (type == "church"): return setOfTags.church
    elif (type == "movie_theater"): return setOfTags.movie_theater
    elif (type == "museum"): return setOfTags.museum
    elif (type == "night_club"): return setOfTags.night_club
    elif (type == "park"): return setOfTags.park
    elif (type == "restaurant"): return setOfTags.restaurant
    elif (type == "synagogue"): return setOfTags.synagogue
    elif (type == "tourist_attraction"): return setOfTags.tourist_attraction
    elif (type == "point_of_interest"): return setOfTags.point_of_interest
    elif (type =="establishment"): return setOfTags.establishment

def modifyRatings(monuments):
    LIMIT_OF_RESULTS=5
    for monument in monuments:
        ## sprawdź historię

        history=History.query.filter_by(UserID=current_user.id).limit(LIMIT_OF_RESULTS) #biorę pod uwagę tylko 5 ostatnich wyborów

        for i in range(0,history.count()):
            if history[i].chosenMonument == monument.name: #nwm, cokolwiek
                monument.rating+=10.0/(i+1)
        
        ## patrząc na preferencje użytkownika
        setOfTags = Tags.query.filter_by(UserID = current_user.id).first()

        for type in monument.types:
            if type in whole_list:
                monument.rating+=5*GetValueOfType(type, setOfTags)
    return monuments

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
    modifyRatings(monuments) # potęzny algorytm obliczania ratingu
    monuments.sort(key=lambda x: x.rating, reverse=True)

    cache.set('monuments', monuments)
    cache.set('sourceLatitude', latitude)
    cache.set('sourceLongitude', longitude)

    return render_template('foundMonuments.html',monums=monuments)

def FindMonumentByName(monuments, name):
    print('looking for ', name, '...\n')
    for monument in monuments:
        print(monument.name)
        if monument.name == name:
            return monument
    return None

def UpdateSetOfTags(monument, setOfTags):
    for type in monument.types:
        setOfTags.addValue(key=type, value=3) # whatever


@main.route('/chosenMonument')
@login_required
def ChosenMonument():
    chosen=request.args.get('monument')
    destLatitude=request.args.get('latitude')
    destLongitude=request.args.get('longitude')
    #add to history
    max_id = db.session.query(func.max(History.id)).scalar()
    idx=-1
    if max_id:
        idx=max_id+1
    else:
        idx=1
    history = History(id=idx, UserID=current_user.id, chosenMonument=chosen)
    # add the new user to the database
    db.session.add(history)
    db.session.commit()

    #update preferences
    setOfTags = Tags.query.filter_by(UserID = current_user.id).first()
    print(cache.get('monuments'))
    monuments=cache.get('monuments')
    monument=FindMonumentByName(monuments, chosen)
    UpdateSetOfTags(monument, setOfTags)
    ## TODO:mapka google która wyznacza Ci trasę,jak dotrzesz to wykorzystać czytanie wikipedii głosem IVONY

    textToSay=getInfoString(chosen)
    
    return render_template('chosenMonument.html', choice=chosen, sourceLat=cache.get('sourceLatitude'),
     sourceLong=cache.get('sourceLongitude'), destLat=destLatitude,
    destLong=destLongitude, text=textToSay) 
