sturnus
=======

django database &amp; website for experiment data

# Quickstart

1. make sure you are running Python 2.7
2. install virtualenv & virtualenvwrapper
3. make sure you [have access to pg_config locally]([)https://www.google.com/search?q=psycopg2+pg_config+executable+not+found) 
4. then, setup your virtual environment
```bash
mkvirtualenv --no-site-packages --distribute sturnus
```
5. and install the requirements
```bash
pip install -r requirements.txt
```
6. setup a local development database
7. run ```./manage.py syncdb --all``` to build the database
8. run ```./manage.py migrate --fake``` to run the south migrations

