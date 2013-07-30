sturnus
=======

django database &amp; website for experiment data

# Quickstart

1. make sure you are running Python 2.7
2. install virtualenv & virtualenvwrapper
3. make sure you [have access to pg_config locally](https://www.google.com/search?q=psycopg2+pg_config+executable+not+found) 
4. then, setup your virtual environment
```Bash
mkvirtualenv --no-site-packages --distribute sturnus
```
5. and install the requirements
```Bash
pip install -r requirements.txt
```
6. setup a local development database
7. run ```./manage.py syncdb --all``` to build the database
8. run ```./manage.py migrate --fake``` to run the south migrations

# Goals

1. Maintain the core electrophysiology data in a neo-compatible format
2. Modularize experimental components
3. Make data easily available for analysis in Matlab & Python (& R?)

# Approach
1. data maintained using Django ORM + PostgreSQL database
2. utilize Postgres arrays for array data (LFP, spike waveforms, intracellular traces)
2. each experimental module developed as a separate Django 'app'
3. data available for querying from external services through the Tastypie RESTful API
4. data overview & exploration through django admin interface