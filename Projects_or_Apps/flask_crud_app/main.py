from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///users.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# Model for User
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)

# Create Database
with app.app_context():
    db.create_all()

# Home - Show All Users
@app.route("/")
def index():
    users = User.query.all()
    return render_template("index.html", users=users)

# Create User
@app.route("/add", methods=["POST"])
def add_user():
    name = request.form["name"]
    email = request.form["email"]
    new_user = User(name=name, email=email)
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for("index"))

# Update User
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_user(id):
    user = User.query.get(id)
    if request.method == "POST":
        user.name = request.form["name"]
        user.email = request.form["email"]
        db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit.html", user=user)

# Delete User
@app.route("/delete/<int:id>")
def delete_user(id):
    user = User.query.get(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080,debug=True)
