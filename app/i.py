import json
from datetime import date, datetime, timedelta
from scipy import stats

from flask import Flask, abort, request, jsonify, url_for, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_login import UserMixin
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.config["SECRET_KEY"] = "top secret"
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["ENV"] = "development"

db = SQLAlchemy(app)
auth = HTTPBasicAuth()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(200))

    def set_password(self, password):
    	self.password_hash = generate_password_hash(password, method='sha256') #dont store cleartext

    def verify_password(self, password):
    	return check_password_hash(self.password_hash, password)

def get_date():
	return datetime.now()

class Mood(db.Model):
	__tablename__ = 'moods'
	id = db.Column(db.Integer, primary_key=True)
	uid = db.Column(db.Integer, db.ForeignKey(id))
	mood = db.Column(db.String(32))
	created = db.Column(db.Date, default=get_date)
	streak = db.Column(db.Integer)

#Callback for auth.login_required guard
@auth.verify_password
def verify_password(username, password):    
    user = User.query.filter_by(username=username).first()
    if not user or not user.verify_password(password):
        return False
    g.user = user #this allows you to use logged in user downstream
    return True

@app.route('/mood', methods=['GET', 'POST'])
@auth.login_required
def mood():
	#GET
	if request.method == 'GET':
		r = Mood.query.filter_by(uid=g.user.id).all()
		if not r:			
			return ({'r': 'No Moods available', 'username': g.user.username}, 201)
		else:
			#janky percentile rank
			e = db.session.query(Mood.uid, db.func.max(Mood.streak)).group_by(Mood.uid).all()
			for element in e:
				if element[0] == g.user.id:
					u_streak = element[1]

			e = [g[0] for g in e]
			p = stats.percentileofscore(e, u_streak)
			if p >= 50.0:
				return ({'r': [{'id': mood.id, 'uid': mood.uid, 'mood': mood.mood, 'created': mood.created, 'streak': mood.streak} for mood in r], 'username': g.user.username, 'percentile': p}, 201)
			else:
				return ({'r': [{'id': mood.id, 'uid': mood.uid, 'mood': mood.mood, 'created': mood.created, 'streak': mood.streak} for mood in r], 'username': g.user.username}, 201)
	#POST
	elif request.method == 'POST':
		yesterday = date.today() - timedelta(days = 1)
		r = Mood.query.filter_by(uid=g.user.id).filter(Mood.created == yesterday).first()
		if not r:
			mood = Mood(mood=request.json.get('mood'), uid=g.user.id, streak=1)
		else:
			s = r.streak + 1
			mood = Mood(mood=request.json.get('mood'), uid=g.user.id, streak=s)

		db.session.add(mood)
		db.session.commit() 
		
		return ({'success': True, 'streak': mood.streak})
	

@app.route('/api/users', methods=['POST'])
def new_user():
    username = request.json.get('username')
    password = request.json.get('password')
    if username is None or password is None:
        abort(400)
    if User.query.filter_by(username=username).first() is not None:
        abort(400)
    user = User(username=username)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()
    return (jsonify({'username': user.username}), 201)

if __name__ == "__main__":
		app.run(host="0.0.0.0", port="1337") #port of your choice make sure it's open
