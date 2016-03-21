# python-getting-started

A barebones Python app, which can easily be deployed to Heroku.

This application supports the [Getting Started with Python on Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) article - check it out.

## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org).  Also, install the [Heroku Toolbelt](https://toolbelt.heroku.com/) and [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ git clone git@github.com:moxgreen/funcpred.git
$ sudo apt-get install libmysqlclient-dev
$ sudo apt-get install python-dev
$ cd python-getting-started

$ pip install -r requirements.txt

$ #createdb python_getting_started
$ configure the database and set DATABASE_URL in .env

$ heroku local:run ./manage.py migrate
$ python manage.py collectstatic

$ heroku local web
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

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)

# caricare dati sul mysql server
xavier:/raid/molineri/bioinfotree/prj/lncrna2function_clone/dataset/gtex_single_tissue_log.GO.noIEA.BP/all_tissues
$ echo "LOAD DATA LOCAL INFILE 'db_Function.2' INTO TABLE funcpred_function" | mysql --local-infile -u funcpred -p -h 130.192.147.6 funcpred

# configurazione apache
vedi il file apache.conf 
