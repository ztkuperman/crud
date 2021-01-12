# Basic CRUD blog app.
Written in flask, using SQLAlchemy.
Doesn't have any tests in the repo.
Does work, but has some rough edges/missing features.

# Building
(This might not be 100%)
Clone the repo. Delete db/crud.sqlite. Run the app with python app.py. When it initializes the DB, it will print the admin credentials to the terminal.

# Components
## Talk Python Training
I followed Talk Python's "Build a data-driven web app in Flask" to learn how to build a Flask web app.
Certain design patterns, like the folder layout and viewmodels are entirely Michael Kennedy's.
The course was definitely worth taking.
## SQLAlchemy
This is used to hold user and blog info. It uses a SQLite db on the filesytem.
## Redis (Filesystem cache)
Redis is used to hold the user sessions. It uses a filesystem cache. (Easier for dev than setting up a redis server)
By default, Flask stores the session info in cookies on the browser. I wanted to keep sensitive info in the session, so I used flask-session to move the session to server side.
## TinyMCE
TinyMCE is an open-source WYSIWYG editor for creating/editing posts.
## Oso
Oso is a policy engine for handling permissions. It keeps permission checking out of your code and allows you to add a lot of complexity to permissions without much difficulty. I used it because the same day I was writing the code for permissions, I heard an interview with Oso on Talk Python to Me. https://www.osohq.com/
