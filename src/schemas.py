from models import User, Movie
from main import ma
from marshmallow.validate import Length

class MovieSchema(ma.Schema):
  class Meta:
    #fields that would be exposed
    fields = ("title", "description", "release_date", "runtime")

#for one card retrieval 
movie_schema = MovieSchema()

#for multiple cards retrieval
movies_schema = MovieSchema(many=True)

class UserSchema(ma.SQLAlchemyAutoSchema):
  class Meta:
    model = User
  #validate password length  
  password = ma.String(validate=Length(min=6))
    
#for one card retrieval 
user_schema = UserSchema()

#for multiple cards retrieval
users_schema = UserSchema(many=True)