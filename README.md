#Setup:

pip3 install requirements.txt
create .env file in directory end enter the following: export TMDB_API_KEY=

#To run app:

python3 routes.py


#Technologies used

Flask framework: utilized the jinja template engine to display information on a HTML page.

imported flask (framework) requests (used to allow API calls) os (necessary for hiding sensitive information in our .env [i.e API keys, database codes, etc]) random (used to return random movie ID's for the index.html page) base64

TMDB API used to request movie information to be displayes (tagline, title, description, genre, etc.) WIKI API used to return a Wikipedia link to the desired movie

Postgressql used to store user login information as well as user comment/rate information for each user.
