import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    messagehistory = db.Column(db.ARRAY(db.Integer), nullable=True)
    firstname = db.Column(db.String, nullable=False)
    lastname = db.Column(db.String, nullable=False)
    #update, delete and update tables
    email = db.Column(db.String, nullable=False)
    #basically given an id linking to logins table id
    password = db.Column(db.String, nullable=False)



class Messages(db.Model):
    __tablename__ = "messagings"
    id = db.Column(db.Integer, primary_key=True)
    day = db.Column(db.Integer, nullable=False)
    month = db.Column(db.String, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    timesent = db.Column(db.String, nullable=False)
    messagecontent = db.Column(db.String, nullable=False)
    sender = db.Column(db.String, nullable=False)
