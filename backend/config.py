import os

# Database initialization
basedir = os.path.abspath(os.path.dirname(__file__))+"/.."
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data/places.db')
SECRET_KEY = "\xd5PE\xa3t\x96D\xa2\xae\xc2\xcfIq\xe7\xefk"
