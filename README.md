
**Overview**

This project will enable a user to add movies along with their directors and genres to a database through a Flask app. Through various routes, the user will also be able to view the total number of movies, see all the contents of the database in the form of a list, and view a surprise message.

Information accessible to the user through various routes include:
* Number of movies in the database
* All contents of the database
* Surprise message


**How it works**
<br>There is one main files involved in running this application.

* SI507_project3.py


**SI507_project3.py**
<br>This file is where the database, as well as the flask application is created using flask_sqlalchemy.

Three tables are created in the database: movies, directors, and genres. The relationships between the tables are as follows:
* Movies to Directors: many to one
* Movies to genres: many to one

Four routes are available to the user in the flask application:
* (/) - Displays the number of movies in the database
* (/movie/new/[name>]/[director]/[genre]/) - Allows the user to add a new movie to the database
* (/all_movies) - Displays all movies in the database along with their respective directors and genres
* (/other) - Displays a surprise message


**Running the application**<br>
In order to run the application, the user must first install everything included in requirements.txt.
Then the user must run the SI507_project3 file by going into the containing directory and typing in 'python3 SI507_project3.py' This will initiate the application after which the user can go into their web browser and access the routes created in SI507_project3.py.

In the web browser the user should type in this address followed by the route they are interested in: localhost:5000/

For example, after running the SI507_project3.py in the command prompt, if the user is interested seeing all movies in the database, they should visit *localhost:5000/all_movies* in their web browser.
