import os
from flask import Flask
from application.database import db

from flask_restful import Resource, Api
curr_dir=os.path.abspath(os.path.dirname(__file__))

from application.api import UserAPI, ListAPI, CardAPI, SummaryAPI

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"+os.path.join(curr_dir, "local_db.sqlite3")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
api=Api(app)
app.app_context().push()
if not os.path.exists(os.path.join(curr_dir, "local_db.sqlite3")):
    db.create_all(app=app)

from application.controllers import *

api.add_resource(UserAPI, "/api/user/<string:username>", "/api/user")
api.add_resource(ListAPI, "/api/list/<int:list_id>", "/api/list")
api.add_resource(CardAPI, "/api/card/<int:card_id>", "/api/card")
api.add_resource(SummaryAPI, "/api/summary/<int:sum_id>")


if __name__=="__main__":
    app.debug=True
    app.run()