from models import User
from main import ma
from marshmallow.validate import Length
from marshmallow import fields

class MovieSchema(ma.Schema):
  class Meta:
    ordered = True
    #fields that would be exposed
    fields = ("title", "description", "release_date", "runtime")

#for one card retrieval 
movie_schema = MovieSchema()

#for multiple cards retrieval
movies_schema = MovieSchema(many=True)

class UserSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    ordered = True
    model = User
    fields = ("id", "name", "email", "password", "admin", "join_date", "reviews")
    load_only = ("password", "admin")
  #validate password length  
  password = ma.String(validate=Length(min=6))
  reviews = fields.List(fields.Nested("ReviewSchema", only=("title", "movie", "rating")))

#for one card retrieval 
user_schema = UserSchema()

#for multiple cards retrieval
users_schema = UserSchema(many=True)

class ReviewSchema(ma.Schema):
  class Meta:
    #fields that would be exposed
    ordered = True
    fields = ("id", "title","post_date", "comment", "rating", "movie", "user")
  user = fields.Nested("UserSchema", only=("name", "email"))
  movie = fields.Nested("MovieSchema", only=("title", "release_date"))

#for one card retrieval 
review_schema = ReviewSchema()

#for multiple cards retrieval
reviews_schema = ReviewSchema(many=True)