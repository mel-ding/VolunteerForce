import os

from flask import Flask
from flask import render_template
from flask import request
from flask import redirect

from flask_sqlalchemy import SQLAlchemy

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "volunteers.db"))

# initialize flask application
app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SQLALCHEMY_DATABASE_URI"] = database_file
db = SQLAlchemy(app)

class User(db.Model):
    username = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
    status = db.Column(db.Boolean, nullable=False, default=True)
    
    def __repr__(self):
        return "<User: {}>".format(self.username)

# loads home page 
@app.route("/", methods=["GET", "POST"])
def home():
    if request.form:
        volunteer = User(username=request.form.get("name"))
        db.session.add(volunteer)
        db.session.commit()
    volunteers=User.query.all()
    return render_template("home.html", volunteers=volunteers)

# updates volunteer name
@app.route("/update", methods=["POST"])
def update():
    newname = request.form.get("newname")
    oldname = request.form.get("oldname")
    volunteer = User.query.filter_by(username=oldname).first()
    volunteer.username = newname
    db.session.commit()
    return redirect("/")

# deletes volunteer
@app.route("/delete", methods=["POST"])
def delete():
    name = request.form.get("name")
    volunteer = User.query.filter_by(username=name).first()
    db.session.delete(volunteer)
    db.session.commit()
    return redirect("/")

# return back to home template
@app.route("/home", methods=["POST"])
def return_home():
    return redirect("/")

# lead to checkin/checkout template
@app.route("/status", methods=["POST"])
def status():
    volunteers=User.query.all()
    return render_template("status.html", volunteers=volunteers)

# checkin and checkout users 
@app.route('/checkin', methods=["GET", "POST"])
def checkin():
    if request.method == "POST":
        name = request.form.get("name")
        volunteer = User.query.filter_by(username=name).first()
        new_status = not volunteer.status
        volunteer.status = new_status
        db.session.commit() 
        return status()

if __name__ == "__main__":
    app.run(debug=True)