import os 
from flask import Flask
from flask_security import Security, SQLAlchemyUserDatastore, hash_password
from config import Config
from models import db, User, Role

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

def seed(app):
    datastore = app.security.datastore
    for name in ["admin", "examiner", "student"]:
        datastore.find_or_create_role(name=name)
    if not datastore.find_user(email="admin@emp.com"):
        datastore.create_user(email="admin@emp.com", password=hash_password("Admin@123"),
                              f_name="Admin", l_name="User", roles=["admin"])
    db.session.commit()

def create_app() :
    app = Flask(__name__,instance_path=os.path.join(BASE_DIR, "instance"))
    app.config.from_object(Config) ## This copies all the settings here.
    db.init_app(app)

    datastore = SQLAlchemyUserDatastore(db, User, Role)
    app.security = Security(app, datastore)
    
    with app.app_context():
        db.create_all()
        seed(app)
    return app

app = create_app()

@app.route("/api/auth/ping")
def ping():
    return {"message": "pong"}

if __name__ == "__main__":
    app.run(debug=True)