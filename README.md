# AgDSS
  Django based Agricultural Decision Support System (AgDSS) for robotic sampling in precision agriculture.
  Please note that this documentation is incomplete and may be out of date.


##Setup
1. Required software:
  * Python2 (Python3 untested)
  * Django
  * Postgres (or other database, though using another database requires changing code). Set port to 5432 (or change code to reflect chosen port).
  * psycopg2 (required for Postgres)
2. Clone this repo (and navigate to it).
3. Create a (Postgres) database called `agdss` which has a user `aguser` with a password `aguser` (with all permissions). To change these configurations, see `DATABASE` in aguser/settings.py.
  * If on Windows, one may be required to create a Firewall inbound rule allowing traffic on port 5432 as it is closed by default. This may not be necessary, but attempt if there is a problem. 
5. Run `python manage.py migrate`.
6. To create admin credentials (required to access /admin), run `python manage.py createsuperuser` and enter the requested information.
7. To start server, run `python manage.py runserver`.
8. The webapp can then be accessed at [http://localhost:8000](http://localhost:8000). For a list of available pages, see the file agdss/urls.py.
