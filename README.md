# AgDSS
  Django based Agricultural Decision Support System (AgDSS) for robotic sampling in precision agriculture.
  Please note that this documentation is incomplete and may be out of date.


##Setup
1. Required software:
  * Python2 (Python3 untested)
  * Django
  * Postgres (or other database, though using another database requires changing code). Set port to 5432 (or change code to reflect chosen port).
2. If on Windows, one may be required to create a Firewall inbound rule allowing traffic on port 5432 as it is closed by default.
3. To start server, run `python manage.py runserver`.
4. The webapp can then be accessed at [http://localhost:8000](http://localhost:8000). For a list of available pages, see the file agdss/urls.py.
