# coding: utf-8

import os
from .api_rest import app
from flask_sqlalchemy import SQLAlchemy
import datetime
import logging as lg

db = SQLAlchemy(app)

# modèle pour les lieux dans la BDD
class Content(db.Model):
    geonameid = db.Column(db.String, primary_key=True)
    name = db.Column(db.String, nullable=False)
    asciiname = db.Column(db.String, nullable=False)
    alternatenames = db.Column(db.String, nullable=False)
    latitude = db.Column(db.String, nullable=False)
    longitude = db.Column(db.String, nullable=False)
    feature_class = db.Column(db.String, nullable=False)
    feature_code = db.Column(db.String, nullable=False)
    country_code = db.Column(db.String, nullable=False)
    cc2 = db.Column(db.String, nullable=False)
    admin1_code = db.Column(db.String, nullable=False)
    admin2_code = db.Column(db.String, nullable=False)
    admin3_code = db.Column(db.String, nullable=False)
    admin4_code = db.Column(db.String, nullable=False)
    population = db.Column(db.String, nullable=False)
    elevation = db.Column(db.String, nullable=False)
    dem = db.Column(db.String, nullable=False)
    timezone = db.Column(db.String, nullable=False)
    modification_date = db.Column(db.String, nullable=False)

    def __init__(self, geonameid, name, asciiname="", alternatenames="", latitude="", longitude="", feature_class="", feature_code="", country_code="", cc2="", admin1_code="", admin2_code="", admin3_code="", admin4_code="", population="", elevation="", dem="", timezone="", modification_date=datetime.date.today()):
        self.geonameid = geonameid
        self.name = name
        self.asciiname = asciiname
        self.alternatenames = alternatenames
        self.latitude = latitude
        self.longitude = longitude
        self.feature_class = feature_class
        self.feature_code = feature_code
        self.country_code = country_code
        self.cc2 = cc2
        self.admin1_code = admin1_code
        self.admin2_code = admin2_code
        self.admin3_code = admin3_code
        self.admin4_code = admin4_code
        self.population = population
        self.elevation = elevation
        self.dem = dem
        self.timezone = timezone
        self.modification_date = modification_date

    def to_json(self):
        row = {}
        row['geonameid'] = self.geonameid
        row['name'] = self.name
        row['asciiname'] = self.asciiname
        row['alternatenames'] = self.alternatenames
        row['latitude'] = self.latitude
        row['longitude'] = self.longitude
        row['feature_class'] = self.feature_class
        row['feature_code'] = self.feature_code
        row['country_code'] = self.country_code
        row['cc2'] = self.cc2
        row['admin1_code'] = self.admin1_code
        row['admin2_code'] = self.admin2_code
        row['admin3_code'] = self.admin3_code
        row['admin4_code'] = self.admin4_code
        row['population'] = self.population
        row['elevation'] = self.elevation
        row['dem'] = self.dem
        row['timezone'] = self.timezone
        row['modification_date'] = self.modification_date
        return row


# fonction pour initialiser la BDD à partir du fichier txt
def init_db():
    db.drop_all()
    db.create_all()
    with open(os.path.join("data", "FR.txt"), "r", encoding="utf8") as data_file:
        for line in data_file:
            geonameid, name, asciiname, alternatenames, latitude, longitude, feature_class, feature_code, country_code, cc2, admin1_code, admin2_code, admin3_code, admin4_code, population, elevation, dem, timezone, modification_date = line.strip().split('\t')
            db.session.add(Content(geonameid, name, asciiname, alternatenames, latitude, longitude, feature_class, feature_code, country_code, cc2, admin1_code, admin2_code, admin3_code, admin4_code, population, elevation, dem, timezone, modification_date))
    db.session.commit()
    lg.warning('Database initialized!')
