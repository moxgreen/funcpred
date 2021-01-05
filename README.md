```sh
$ apt-get install git apache2 libapache2-mod-wsgi python-virtualenv python-dev libmysqlclient-dev mysql-server
$ git clone git@github.com:moxgreen/funcpred.git
$ sudo mv funcpred /var/www
$ sudo chgrp www-data -R /var/www/funcpred
$ cd /var/www/funcpred
$ virtualenv env
$ source env/bin/activate
$ pip install -r requirements.txt
$ mysql -u root -p -h localhost
mysql> create database funcpred2
mysql> GRANT ALL PRIVILEGES ON funcopred2.* To 'funcpred2'@'localhost' IDENTIFIED BY 'funcpred';
mysql> flush privileges;

$ ssh funcored.com 'mysqldump -u funcpred2 -p funcpred2 | gzip ' | zcat | mysql -u funcpred2 -p funcpred2
$ # configure the database and set DATABASE_URL in .env or settings.py

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
