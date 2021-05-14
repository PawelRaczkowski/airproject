from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/profile')
@login_required
def profile():

    #from .models import Tags
    #
    #tag = Tags.query.filter_by(UserID=current_user.ID).first()
    #if not tag:
    #    return render_template('TagSetting.html')

    return render_template('profile.html', name=current_user.login)

#@main.route('/TagSetting', methods=['POST'])
#@login_required
#def createPreferences():
#    args = request.args
#
#    from .models import Tags
#    newPreference = Tags(UserID = current_user.ID)
#
#    for arg in args:
#        #nie wiem jak będziemy przekazywać tagi, a że na froncie sięnie znam, to nie będę na ślepo implementował :p
#        #newpreference.setValue(arg.key, 20)
#   
#    db.session.add(newPreference)
#    db.session.commit()
#    return render_template('profile.html', name=current_user.login)