from main import db

class User(db.Model):
    #table name in the database
    __tablename__ = "USERS"

    #primary key
    id = db.Column(db.Integer, primary_key=True)
    #other attributes
    user_name = db.Column(db.String(30), nullable=False)
    join_date = db.Column(db.Date(), nullable=False)

    # one-to-many relationships to other models, include back reference
    reviews = db.relationship('Review', backref='user')
    lists = db.relationship('List', backref='user')

    #gives each object a string representation for debugging purposes
    def __repr__(self):
        return f'<User "{self.user_name}>'

class Movie(db.Model):
    #table name in the database
    __tablename__ = "MOVIES"

    #primary key
    id = db.Column(db.Integer, primary_key=True)
    #other attributes
    movie_name = db.Column(db.String(), nullable=False)
    release_date = db.Column(db.Date(), nullable=False)
    director = db.Column(db.String(30), nullable=False)
    about = db.Column(db.String(300), nullable=False)
    genre = db.Column(db.String(30))

    # one-to-many relationships to other models, include back reference
    reviews = db.relationship('Review', backref='movie')
    movies_in_list = db.relationship('MovieInList', backref='movie')

    #gives each object a string representation for debugging purposes
    def __repr__(self):
        return f'<Movie "{self.movie_name}>'


class Review(db.Model):
    #table name in the database
    __tablename__ = "REVIEWS"

    #primary key
    id = db.Column(db.Integer, primary_key=True)
    #other attributes
    title = db.Column(db.String(100), nullable=False)
    comment = db.Column(db.String())
    rating = db.Column(db.Integer(), nullable=False)
    #foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))

    #gives each object a string representation for debugging purposes
    def __repr__(self):
        return f'<Review "{self.title}>'

class List(db.Model):
    #table name in the database
    __tablename__ = "LISTS"

    #primary key
    id = db.Column(db.Integer, primary_key=True)
    #other attributes
    title = db.Column(db.String())
    publish_date = db.Column(db.Date())
    #foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # one-to-many relationships to other models, include back reference
    movies_in_list = db.relationship('MovieInList', backref='list')

    #gives each object a string representation for debugging purposes
    def __repr__(self):
        return f'<List "{self.title}>'

class MovieInList(db.Model):
    #table name in the database
    __tablename__ = "MOVIES IN LIST"

    #primary key
    id = db.Column(db.Integer, primary_key=True)
    #other attributes
    comment = db.Column(db.String())
    #foreign keys
    list_id = db.Column(db.Integer, db.ForeignKey('list.id'))
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))