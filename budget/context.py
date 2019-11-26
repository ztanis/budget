from flask import Flask

from flask_sqlalchemy import SQLAlchemy

# Create application
app = Flask(__name__)

# Create dummy secrey key so we can use sessions
app.config['SECRET_KEY'] = '123456790'

# Create in-memory database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/budget'
db = SQLAlchemy(app)
