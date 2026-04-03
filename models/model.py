
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



db = SQLAlchemy()



class User(db.Model):
     uid = db.Column(db.Integer, primary_key=True)
     uname =db.Column(db.String(200), unique=True, nullable = False )
     upass = db.Column(db.String(200), nullable= False)

class BlogContant(db.Model):
     blogId = db.Column(db.Integer, primary_key = True)
     title = db.Column(db.String(200), nullable=False )
     contant = db.Column(db.Text, nullable=False)
     clreated_at =db.Column(db.DateTime, default= datetime.utcnow)
     auther = db.Column(db.String(200), nullable=False)



