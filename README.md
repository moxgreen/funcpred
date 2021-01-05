```sh
$ apt-get install gcc git apache2 libapache2-mod-wsgi virtualenv python-dev libmysqlclient-dev libmariadb-dev libmariadb-dev-compat mysql-server
$ git clone git@github.com:moxgreen/funcpred.git
$ sudo mv funcpred /var/www
$ sudo chgrp www-data -R /var/www/funcpred
$ cd /var/www/funcpred
$ virtualenv -p /usr/bin/python2.7 env
$ source env/bin/activate
$ pip install -r requirements.txt
sudo mysql --defaults-file=/etc/mysql/debian.cnf
mysql> create database funcpred2;
mysql> CREATE USER 'funcpred2'@'localhost' IDENTIFIED BY 'funcpred';
mysql> ALTER USER 'funcpred2'@'localhost' IDENTIFIED WITH mysql_native_password BY 'funcpred';
mysql> GRANT ALL PRIVILEGES ON funcopred2.* To 'funcpred2'@'localhost';
mysql> flush privileges;

$ ssh funcpred.com 'mysqldump -u funcpred2 -p funcpred2 | gzip ' | zcat | mysql -u funcpred2 -p funcpred2
# configure the database and set DATABASE_URL in .env or settings.py
```
# caricare dati sul mysql server
xavier:/raid/molineri/bioinfotree/prj/lncrna2function_clone/dataset/gtex_single_tissue_log.GO.noIEA.BP/all_tissues
$ echo "LOAD DATA LOCAL INFILE 'db_Function.2' INTO TABLE funcpred_function" | mysql --local-infile -u funcpred -p -h 130.192.147.6 funcpred

# configurazione apache
vedi il file apache.conf 
