# Python: Getting Started

A barebones Django app, which can easily be deployed to Heroku.

This application supports the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out.

## Running Locally

Make sure you have Python 3.7 [installed locally](http://install.python-guide.org). To push to Heroku, you'll need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli), as well as [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ git clone https://github.com/heroku/python-getting-started.git
$ cd python-getting-started

$ python3 -m venv getting-started
$ pip install -r requirements.txt

$ createdb python_getting_started

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local - for linux
$ heroku local web -f Procfile.windows - for win
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ heroku create
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)


## Add functionality OPENCV to heroku:
1. install heroku-buildpack-apt:
https://elements.heroku.com/buildpacks/heroku/heroku-buildpack-apt

```sh
$ heroku buildpacks:add --index 1 heroku-community/apt
```
2. Create Aptfile with content:
libsm6
libxrender1
libfontconfig1
libice6

3. The end

## Disable collect static:
 $ heroku config:set DISABLE_COLLECTSTATIC=1


## Download: heroku git:clone -a myapp

## CLEAR DB
Step 1: heroku restart
Step 2: heroku pg:reset DATABASE (no need to change the DATABASE)
Step 3: heroku run rake db:migrate
Step 4: heroku run rake db:seed (if you have seed)

## LOGS:
heroku logs --source app --dyno worker -n 200
heroku logs -t --source app

## Chage redirect address from 127.0.0.1 to nenuz.com:
in the file system32/drivers/etc/hosts type:
``127.0.0.1 nenuz.com``
in cmd run "ipconfig /flushdns" - it will clear dns cache
Then turn off vpn in browser (opera)!
Profit!

## Antonio Mele Django by example book source:
https://github.com/guinslym/django-by-example-book/tree/master/Django_By_Example_Code

## Dump and load data
Dump data:
```
python manage.py dumpdata account images auth.User pizzashopapp --indent 4 -o db.json
```
Load data:
```
python manage.py loaddata db.json
```

## Product shop functionality
chap 1.
• Creating the product catalog models, adding them to the administration site,
and building the basic views to display the catalog
• Building a shopping cart system using Django sessions to allow users
to keep selected products while they browse the site
• Creating the form and functionality to place orders
• Sending an asynchronous email confirmation to users when they place
an order

chap 2.
• Integrate a payment gateway into your project
• Manage payment notifications
• Export orders to CSV files
• Create custom views for the administration site
• Generate PDF invoices dynamically

chap 3.
• Creating a coupon system to apply discounts
• Adding internationalization to your project
• Using Rosetta to manage translations
• Translating models using django-parler
• Building a product recommendation engine

## E-Learning platform
Chap 1.
• Create fixtures for models
• Use model inheritance
• Create custom model fields
• Use class-based views and mixins
• Build formsets
• Manage groups and permissions
• Create a CMS
    - Log in to the CMS
    - List the courses created by the instructor
    - Create, edit, and delete courses
    - Add modules to a course and reorder them
    - Add different types of content to each module and reorder
    contents
    
Chap 2.
• Create public views for displaying course information
• Build a student registration system
• Manage student enrollment in courses
• Render diverse course contents
• Cache content using the cache framework
    - install memcached on Linux: ./configure && make && make test && sudo make install
                        on Win: https://www.ubergizmo.com/how-to/install-memcached-windows/ 
    - start memcached on Lin: memcached -l 127.0.0.1:11211
                      on Win: memcached start
                      (defaul port == 127.0.0.1:11211)
                        
Chap 3.
• Building an API
    Retrieve subjects
    Retrieve available courses
    Retrieve course contents
    Enroll in a course
• Build a RESTful API
• Handle authentication and permissions for API views
• Create API view sets and routers

## Celery
launch:
```
celery -A gettingstarted worker -l info
```
Web-based celery monitor flower:
```
celery -A gettingstarted flower
```
Now you can watch celery tasks at 
http://localhost:5555/dashboard

## Paypal
Test buyer account email:
``nenuzhny85-buyer@gmail.com``
Test buyer account password
``13245678``

## Localization
1. Add languages to settings.py and
create folders "en" and "ru" in the "locale" folder;
2. run: ``django-admin makemessages --all --ignore venv``
3. edit msgstr variable in the files django.po for each locale
4. run ``django-admin compilemessages``
