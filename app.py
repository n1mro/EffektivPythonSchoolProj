from flask import Flask
from models import db, seed_data
from flask_migrate import Migrate, upgrade
from views import home, persons



app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')

db.app = app
db.init_app(app)
migrate = Migrate(app, db)  

app.register_blueprint(home, url_prefix='/')
app.register_blueprint(persons, url_prefix='/person')

if __name__ == "__main__":
    with app.app_context():
        upgrade()
        seed_data(db)
    app.run()