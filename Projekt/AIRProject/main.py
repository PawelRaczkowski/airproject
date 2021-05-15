from flask import Blueprint, render_template
from flask_login import login_required, current_user
from flask import request
from . import db


# URL for search: https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=-33.8670522,151.1957362&radius=1500&type=restaurant&key=YOUR_API_KEY

main = Blueprint('main', __name__)

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
    return render_template('searchMonuments.html')


@main.route('/searchMonuments', methods=['POST'])
@login_required
def getMonuments(): # na razie zaślepka
    args = request.args
    return render_template('foundMonuments.html', monuments=args)


