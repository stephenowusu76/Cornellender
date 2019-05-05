from flask_sqlalchemy import SQLAlchemy

db=  SQLAlchemy()


association=db.Table('events',db.Model.metadata,
db.Column('event_id',db.Integer,db.ForeignKey('event.id')),
db.Column('user_id',db.Integer,db.ForeignKey('user.id'))
)

class Event(db.Model):
    __tablename__='event'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String, nullable=False)
    location=db.Column(db.String,nullable=False)
    longitude=db.Column(db.String,nullable=False)
    latitude=db.Column(db.String,nullable=False)
    tag=db.Column(db.String,nullable=False)
    link=db.Column(db.String,nullable=False)
    image=db.Column(db.String,nullable=False)
    date=db.Column(db.String, nullable=False)
    tag=db.Column(db.String, nullable=False)
    description=db.Column(db.String, nullable=False)
    users=db.relationship('User', secondary=association)


    def __init__(self,**kwargs):
        self.name=kwargs.get('name','')
        self.date=kwargs.get('date','')
        self.tag=kwargs.get('tag','')
        self.description=kwargs.get('description','')
        self.location=kwargs.get('location','')
        self.link=kwargs.get('link','')
        self.image=kwargs.get('image','')
        self.longitude=kwargs.get('longitude','')
        self.latitude=kwargs.get('latitude','')

    def serialize(self):
        return{
            'id': self.id,
            'date':self.date,
            'name': self.name,
            'tag': self.tag,
            'description': self.description,
	    'location':self.location,
	    'link':self.link,
	    'image':self.image,
            'longitude':self.longitude,
	    'latitude':self.latitude
        }

class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String, nullable=False)
    password=db.Column(db.String, nullable=False)
    events=db.relationship('Event', secondary=association)
    

    def __init__(self,**kwargs):
        self.name=kwargs.get('name','')
        self.password=kwargs.get('password','')
 
    def serialize(self):
        return{
            'id': self.id,
            'name':self.name,
            'netid': self.netid,
            'events':[eve.serialize() for eve in self.events] 

        }
    def serialize2(self):
        return{
            'id': self.id,
            'name':self.name,
            'netid': self.netid,
        }    

