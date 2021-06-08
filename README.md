# LITReview

LITReview is a Django platform allowing its registered users to exchange book reviews.

Users can ask for reviews or post reviews in response to tickets published by followed users.

# Run LITReview

## Clone application and install packages

* Clone LITReview application in your target folder: `git clone https://github.com/Alexandremerancienne/LITReview.git`

* Create a virtual environment.

* Activate your venv, then install packages listed in requirements.txt file : `pip install -r requirements.txt`

## Create database and configurate Django

* Create a database - we have used PostgreSQL for this project, but you can use other databases, such as SQLite.

* In LITReview project :

  * Open LITReview/LITReview/settings.py

  * In DATABASES dictionary, complete the following fields with the information about your own database:

    * "ENGINE" (type of database used)
    * "NAME" (name of your database)
    * "USER" (default value "postgres")
    * "PASSWORD" (password to your database)
    * "PORT" (default value "5432")

  * Once the database is configurated, migrate your data: `python manage.py migrate`

## Populate database (optional step, only to test application with fixtures)

If you want to test directly the application without creating users, reviews... you can import fixtures as follows:

* Import users: `python manage.py loaddata litreviewusers.json`
* Import posts: `python manage.py loaddata litreviewusers.json`

## Create a superuser 

* Create a superuser to monitor the administration of the application: `python manage.py createsuperuser`

* Fill the username, the email address and the password of the superuser to finalize registration.

## Start LITReview

* Launch local server from your terminal: `python manage.py runserver`

* Follow the URL to access LITReview website. 
