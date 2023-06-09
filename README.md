## Setup instructions
Welcome to the Movie Review API. Please connect to a PostgreSQL database on your local machine and update the database URI in the .env file. Please download all the packages in requirements.txt in your virtual environment. In src folder, movies.txt contains data on 44,000 movies, this data can be added to the database via the "flask create" followed by "flask db seed" cli command in the terminal, please don't modify this file. Any questions feel free to reach out to johnsonw1017@gmail.com

## R1, R2 Identification of the problem you are trying to solve by building this particular app. Why is it a problem that needs solving?

Movies are time consuming yet time is a priceless commodity. Often the decision-making of choosing the best movie to watch can be frustrating, factoring questions like what movie would provide me with the best experience? how can I maximise the 2 hours I got? do I choose this movie over the other one? etc. The Movie Review API aims to provide answers to these questions by providing all the information about movies and include helpful reviews from other users explaining their experience with the movies. It aims to reduce the time people spent on decision making so they can spend more time enjoying their movie of choice. Additional features of the API include allow users to create lists, this can be a watchlist, a top 10 recommended list, or an organisation tool for movies of different genre. By sharing these lists to other users would also help provide a starting point for those in search of the best movie to watch.

## R3 Why have you chosen this database system. What are the drawbacks compared to others?
PostgreSQL is the database management system used in this API. There is an estimated 500,000 movies available in world (2023). With such a large dataset, PostgreSQL was chosen for its robust features and powerful querying capabilities:
- Supports a wide range of data type such as JSON that are useful for storing large amounts of data
- ACID compliant, ensuring data consistency in the face of failures and issues
- Has full text search functionality, allowing user to search through movies titles with ease
- Finally, it is an open source software, meaning it is free to use and has a community for development support

The drawbacks of PostgreSQL compared to other database include:
- Comparatively more complex them other DBMS requiring a steeper learning curve
- Limited support compared to proprietary DBMS since it relies on community
- Limited ability to handle unstructured data and not capable of storing graphical data

## R4 Identify and discuss the key functionalities and benefits of an ORM
SQLAlchemy is an Object-Relational Mapping (ORM) library for Python and is used in this application. The following are its key functionalities and benefits:

- SQL Expression Language - offers a convenient way to define database queries using basic Python expressions without having to write raw SQL commands.
- Object Relational Mapper - enables developers to work with database entities as Python objects, making it easier to translate between the application and the database.
- Database Abstraction Layer - SQLAlchemy allows developers to work in cross-platform environment without having to change the code
- Query Building - allows building of complex database queries using Python syntax that translates into efficient SQL statements.
- Sessions Management - provides an easy-to-use mechanism for managing database sessions by allowing devs to perform CRUD functions and query data from these sessions without needing to manage connections explicitly.
- Data Validation - has a built-in validation mechanism that automates data verification, ensuring data conforms to a specific schema or format.
- Integration with Web Frameworks - integration support to modern web frameworks such as Flask, Django, Pyramid etc., making it easier for developers to create data-driven web applications.
- Scalability - scalable to handle large datasets, complex queries, and high traffic workloads.

## R5 Document all endpoints for your API
Endpoint documentation should include
 - HTTP request verb
 - Required data where applicable 
 - Expected response data 
 - Authentication methods where applicable

|Endpoint Route|Request method|Functionality|
|---|----|----|
|/profile/{int:user_id}|GET|Returns a User object from the database given the user_id in the route. Returns an error message if the user does not exist. This route is available to non-registered users as well.|
|/profile/{int:user_id}|DELETE|Deletes a User object based on the user_id given in the route. The user must be an admin or the deleted user themself. Authorisation is checked through the user's JWT token. Return the deleted user object in the response upon succession.|
|/profile/{int:user_id}|PUT|Allows users themselves or an admin user to update details about a user in the database, which includes the email, name and password. Returns the updated user object as a response upon succession. Authorisation is checked through the JWT token. The new password is hashed by Flask Bcrypt.|
|/auth/register|POST|Creates a new User object in the database after the user provides information including email, name and password. The join_date value is generated by the datetime.now() function and admin is set to False. The password is hashed by Bcrypt before storing. If the User object is correctly added, the name and access token is returned in the response. The access token has an expiry of one day.|
|/auth/login|POST|Authentication route, where the user enters their email and password to login. The user object is checked to see if it exist within the database and the password is checked to see if it matches. Returns the user's name and a JWT access token upon succession.|
|/movies/{int:movie_id}|GET|Retrieves a Movie object from the database based on the movie_id in the route.This route is available to non-registered users as well.|
|/movies/{int:movie_id}|DELETE|Deletes a Movie object from the database based on the movie_id in the route. Authorised for admin users only where it is checked through the user's JWT token.|
|/movies/{int:movie_id}|PUT|Updates a Movie object in the database in the field of title, runtime, description and release date. Authorised for admin users only where it is checked through the user's JWT token.|
|/movies/top-ten-movies|GET|Returns the top ten Movie objects from the database based the average rating (0-10) from reviews. This was achieved by performing a query that joins the Movie and Reviews table and groups it by the movie id. This route is available to non-registered users as well.|
|/movies/recent-movies|GET|Returns 100 of Movie objects from the database with the most recent release dates, to help users see what may be available in cinemas soon. This route is available to non-registered users as well.|
|/movies/search|GET|Retrieves a Movie object based on a user input of the movie title. Will retrieve all the movies of the same name and an empty list if no names matches the title given. This route is available to non-registered users as well.|
|/movies/{int:movie_id}/reviews|GET|Retrieves the 10 most recent Reviews from the database of a given movies with its movie_id in the route. This route is available to non-registered users as well.|
|/profile/{int:user_id}/reviews|GET|Retrieves the 10 most recent Reviews from the database of a given user with the user_id in the route. This route is available to non-registered users as well.|
|/movies/{int:movie_id}/reviews|POST|Allows registered users to create a review of a Movie object in the database based on the movie_id in the route. Each user can only create one review for each movie. The fields required by the user to input include the title, the comment and the rating.|
|/reviews/{int:review_id}|GET|Retrieves a Review object from the database based on the review_id in the route. This route is available to non-registered users as well.|
|/reviews/{int:review_id}|DELETE|Deletes a Review object from the database based on the review_id given in the route. The user must be an admin user or the review creator. Authorisation is checked through the user's JWT token. Return the deleted review object in the response.|
|/reviews/{int:review_id}|PUT|Updates a Review object in the database based on the review_id given in the route. Fields that can be modified include the title, comment and rating. The user must be an admin user or the review creator. Authorisation is checked through the user's JWT token. Return the deleted review object in the response.|
|/lists|GET|Returns 10 of the most recent Lists from the database that are created by any registered users that is not private. This route is available to non-registered users as well.|
|/lists|POST|Allows registered users to create a List object. Fields required to be input by users include title, comment and the movies. The only field required for adding the movies to the list is the movie.id. The private field is defaulted to False unless the user specify otherwise|
|/profile/{int:user_id}/list|GET|Retrieves all the List objects from the database created by the user with user_id given in the route. Only registered users can access this route. Private lists are only viewable to admin users and the list creator themselves.|
|/lists/{int:list_id}|GET|Retrieves the List object from the database given the list_id in the route. In the case of authorised access to private lists, an error message will return.|
|/lists/{int:list_id}|DELETE|Allow authorised users, the list creator and admin users to delete a List object from the database based on the list_id in the route. Authorisation is achieved by checking the JWT token of the access user.|
|/lists/{int:list_id}|PUT|Allows the list creator and admin user to update certain fields of a List including the title, comment and private fields. Authorisation is achieved by checking the JWT token of the access user.|
## R6 An ERD for your app

![Entity Relationship Diagram](/docs/erd.jpg)

## R7 Detail any third party services that your app will use
| Library/package | version | Description |
|-----------------|---------|-------------|
| bcrypt | 4.0.1 | A python library use hash passwords and store password based on the Blowfish cipher.|
| click | 8.1.3 | A package for creating Command Line Interface (CLI) with multiple options and commands.|
| Flask | 2.2.3 | A Python micro web framework for building web applications.|
| Flask-Bcrypt | 1.0.1 | A Flask extension of bcrypt that helps generate secure passwords and hash them.|
| Flask-JWT-Extended|4.4.4 | A Flask extension that adds support for JSON Web Tokens authentication.|
| flask-marshmallow|0.14.0 | A Flask extension that makes it easier to serialize/deserialize SQLAlchemy ORM objects using Marshmallow.|
| Flask-SQLAlchemy|3.0.3 | A Flask extension that integrates SQLAlchemy into a Flask application.|
| importlib-metadata|6.0.0 |A package to access metadata about packages installed with pip.|
| Jinja2|3.1.2 | A modern and designer friendly templating language for Python, used alongside Flask.|
| marshmallow|3.19.0 | A Python library for converting complex data types, such as objects, to and from native Python data types.|
| marshmallow-sqlalchemy | 0.29.0 | SQLAlchemy integration with the marshmallow serialization/deserialization library.|
| psycopg2|2.9.5 | A PostgreSQL database adapter for the Python programming language.|
| PyJWT|2.6.0 | A Python JWT implementation for authentication|
| python-dotenv|1.0.0 | Reads the key-value pair from .env file and adds them to environment variable.|
| SQLAlchemy|2.0.4 | A library that provides an SQL toolkit and object-relational mapping (ORM) system for Python.|
## R8 Describe your projects models in terms of the relationships they have with each other
The main purpose of the schemas is for validating user inputs in the requests. This includes the fields the users are allowed to input and how the data is organised when it is retrieved for a response. The following includes a brief description of the schemas used for each table (User, Movie, Review and List) in the database and how they relate to each other.

- MovieSchema:
    - Exposed fields: id, title, description, release_date and runtime
    - Nested schema: ReviewSchema where the exposed fields are user and rating
- UserSchema:
    - Exposed fields: id, name, email and join_date
    - Load-only fields: password and admin
    - Nested schemas: ReviewSchema where the exposed fields are title, movie and rating and ListSchema where the exposed field is the title
- ReviewSchema:
    - Exposed fields: id, title, comment and post_date
    - Nested schema: UserSchema where the exposed fields are name and email and MovieSchema where the exposed fields are title and release_date
- ListSchema:
    - Exposed fields: id, title, comment and post_date
    - Load-only fields: private
    - Nested schemas: UserSchema where the exposed fields are name and email and Movie Schema where the exposed fields id, title and release_date

Base on the schema it can be evident that there are:

- One-to-many relationship exist between User and Review: one user to many reviews, yet a review belongs to one user. A foreign key of user_id exist in the Reviews table that references the Users table's id column. Review.user also back references the User object.
- One-to-many relationship exist between User and List: one user to many lists, yet one list belongs to one user. A foreign key of user_id exist in the Lists table that references the Users table's id column. List.user also back references the User object.
- One-to-many relationship exist between Movie and Review: one movie can have many reviews, yet a review is directly linked to one movie. A foreign key of movie_id exist in the Reviews table that references the Movies Table's id column. Review.movie also back references the Movie object.
- Many-to-many relationship exist between Movie and List: A movie can be in many lists, and a list can contain many movies. An association table called movie_list was made to link the two table, which has foreign keys of movie_id and list_id. The Lists Table has a movies attribute, where multiple Movie objects can be linked to a List object through the associations table. 

## R9 Discuss the database relations to be implemented in your application
The movie review API has the following base functionality:
- Allow users to get information on movies and their reviews
- Allow users to create reviews of any given movie
- Allow users to create lists of movies

Based on the ERD, the following are the relationships between the four tables of User, Movie, Review and List.

- User to Review: each user can create many reviews and each review will belong to one user (One-to-Many relationship)
- User to List: each user can create many lists and each list will belong to one user (One-to-Many relationship)
- Movie to Review: each movie can have many reviews and each review will be about one movie (One-to-Many relationship)
- Movie to List: each list can have many movies and each movies can be part of many lists (Many-to-Many relationship)

## R10 Describe the way tasks are allocated and tracked in your project
The project spans over a 3 week period from March 2nd to March 19th 2023. The project was tracked using a Kanban board on Trello (screenshots below). Three columns exist on the Kanban board: to-do, doing and completed. As the project progressed, cards with the task description written on it are moved left to right depending on their status. This was completed daily, and when a card reaches "completed", the completion date is added to the card along with a tick for completion. At the end of each week on the Sunday, a checkpoint is held, almost like a retrospective on the past week and planning ahead for the next. During these checkpoints, the cards are modified to reflect on any project changes.

Trello board at the end of Week 1 (March 6th):
![Trello Board after Week 1](/docs/trello-1.png)

Trello board at the end of Week 3 (March 19th):
![Trello Board after Week 3](/docs/trello-3.png)

As evident on the labels on the cards, the project can be split into five main parts (in chronological order):
1. Project Ideation: this involved coming up with the project, creating the ERD and creating a preliminary project plan.
2. Learning: since this is the first time I created an API on Flask, I allocated some time to learn the overall process on API development in Week 1.
3. Coding Round 1: after configuring the virtual environment, the first coding round involves creating the models, schemas and controllers for User and Movie Tables. At this point, no connection is made between the tables.
4. Coding Round 2: this round involves creating the models, schemas and controllers for the List and Review Table and establishing connections (relationships) to Movie and User.
5. Documentation: creating a README.md file documenting relevant information to the project.

## Additional Information
Main resources used for learning Flask concepts: Ed Lessons provided by Coder Academy, ChatGPT and tutorials on Digital Oceans.

Software used:
- Visual Studio Code - for editing and running source code and managing files
- Postman - for testing routes
- pgAdmin4 - for querying large amount of data when checking functionality

Tech Stack:
- Python Flask - API web framework
- SQLAlchemy - ORM
- PostgreSQL - DBMS