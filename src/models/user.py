from main import db

class User(db.Model):
    #table name in the database
    __tablename__ = "USERS"

    #primary key
    id = db.Column(db.Integer, primary_key=True)

    user_name = db.Column(db.String())
    join_date = db.Column(db.Date())