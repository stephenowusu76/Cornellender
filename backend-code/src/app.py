import json
from db import db, Event, User
from flask import Flask, request

app = Flask(__name__)
db_filename='todo.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///%s' % db_filename
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

db.init_app(app)
with app.app_context():
    db.create_all()



@app.route('/')
def root():
    return 'Hello world!'


@app.route('/api/events/')
def get_all_events():
    events = Event.query.all()
    res = {'success': True, 'data': [eve.serialize() for eve in events]}
    return json.dumps(res), 200

@app.route('/api/event/', methods=['POST'])
def create_event():
    post_body = json.loads(request.data)
    eve = Event(
        name = post_body.get('name'),
        date = post_body.get('date'),
        tag = post_body.get('tag'),
        description = post_body.get('description'),
	location=post_body.get('location'),
	link=post_body.get('link'),
	image=post_body.get('image'),
	latitude=post_body.get('latitude'),
	longitude=post_body.get('longitude')
    )
    db.session.add(eve)
    db.session.commit()
    return json.dumps({'success':True, 'data': eve.serialize()}), 201

@app.route('/api/event/<int:event_id>/')
def get_specific_event(event_id):
    eve = Event.query.filter_by(id=event_id).first()
    if eve is None:
        return json.dumps({'success': False, 'error': 'Task not found'}), 404
    return json.dumps({'success': True, 'data':eve.serialize()}), 200

@app.route('/api/event/<string:tag_t>/')
def get_tag(tag_t):
    eve=Event.query.filter_by(tag=tag_t)
    if eve is None:
        return json.dumps({'success':False, 'error':'Task not found'}), 404
    return json.dumps({'success':True, 'data':[ev.serialize() for ev in eve]}), 200

@app.route('/api/event/<int:event_id>/', methods=['DELETE'])
def delete_event(event_id):
    eve = Event.query.filter_by(id=event_id).first()
    if eve is not None:
        db.session.delete(eve)
        db.session.commit()
        return json.dumps({'success': True, 'data':'DELETED'}), 201
    return json.dumps({'success': False, 'error': 'Task not found'}), 404


@app.route('/api/users/', methods=['POST'])
def create_user():
    post_body = json.loads(request.data)
    user = User(
        name = post_body.get('name'),
        password = post_body.get('password')
    )
    db.session.add(user)
    db.session.commit()
    return json.dumps({'success':True, 'data': user.serialize()}), 201


@app.route('/api/event/<int:event_id>/add/', methods=['POST'])
def add_event(event_id):
    eve = Event.query.filter_by(id=event_id).first()
    if eve is None:
        return json.dumps({'success': False, 'error': 'Task not found'}), 404
    post_body = json.loads(request.data)
    user = User.query.filter_by(id=post_body.get('user_id')).first()
    eve.students.append(user)
    user.events.add(eve)
    db.session.commit()
    return json.dumps({'success': True, 'data':eve.serialize()}), 201



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000, debug=True)
