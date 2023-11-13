from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Sebas911:1qwertyui9.@ebas911.mysql.pythonanywhere-services.com/Shoes_Maker_Inc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = -1

app.secret_key = "mysecretkey"

db = SQLAlchemy(app)
ma = Marshmallow(app)
migrate = Migrate(app, db)
