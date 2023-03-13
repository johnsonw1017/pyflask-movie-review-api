from controllers.movies import movies
from controllers.auth import auth
from controllers.users import users
from controllers.reviews import reviews


registerable_controllers = [
    auth,
    movies,
    users,
    reviews
]