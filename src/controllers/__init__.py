from controllers.movies import movies
from controllers.auth import auth
from controllers.users import users
from controllers.reviews import reviews
from controllers.lists import lists

registerable_controllers = [
    auth,
    movies,
    users,
    reviews,
    lists
]