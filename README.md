# AgDSS
  Django based Agricultural Decision Support System (AgDSS) for robotic sampling in precision agriculture.
  Please note that this documentation is incomplete and may be out of date.


##Setup
1. Required software:
  * Python2 (Python3 untested) with packages NumPy, Pillow, Wand, and django-adminplus
  * Django* < 1.10 (django 1.10 no longer allows you to specify urls as string, http://stackoverflow.com/questions/38744285/django-urls-error-view-must-be-a-callable-or-a-list-tuple-in-the-case-of-includ)
  * * pip install django==1.9
  * Postgres (or other database, though using another database requires changing code). Set port to 5432 (or change code to reflect chosen port). (Setup information: [here](https://help.ubuntu.com/community/PostgreSQL))
  * psycopg2 (required for Postgres)
  * ImageMagick (`ImageMagick 6.7.7-10 Q16` and `ImageMagick-6.9.4 Q16` are known to be working and compatible versions)
  (Tarball for previous versions can be found [here](https://www.imagemagick.org/download/releases/))
2. Clone this repo (and navigate to it).
3. Create a (Postgres) database called `agdss` which has a user `aguser` with a password `aguser` (with all permissions). To change these configurations, see `DATABASE` in aguser/settings.py. The easiest way to do this is through a GUI manager like pgadmin3. However, it can be done via the Unix terminal.
  * If on Windows, one may be required to create a Firewall inbound rule allowing traffic on port 5432 as it is closed by default. This may not be necessary, but attempt if there is a problem.
  * To do this in the terminal, follow the setup information [here](https://help.ubuntu.com/community/PostgreSQL). Afterwords, to create the user, run `sudo -u postgres psql` to enter the postgres prompt. There, run `CREATE USER aguser WITH PASSWORD 'aguser';` followed by `GRANT ALL PRIVILEGES ON DATABASE "agdss" to aguser;`.
  * DB setup on MacOSX:
    psql postgres
    CREATE DATABASE agdss;
    CREATE USER aguser WITH PASSWORD 'aguser';
    GRANT ALL PRIVILEGES ON DATABASE "agdss" to aguser;



5. Run `python manage.py migrate --settings=agdss.settings.prod` to create the tables in the database.
6. To create admin credentials (required to access /admin), run `python manage.py createsuperuser` and enter the requested information.
7. Create a new settings file under '\agdss\settings'. Copy the settings from prod.py and change the `STATIC_ROOT` to point at
a local directory you want the server to access. 
8. TEMPORARY: Set `STATIC_ROOT` to parent directory of images (in agdss/settings.py).
9. TEMPORARY: Place all images directly in directory named `tag_images` which is a child of the `STATIC_ROOT` directory. (The images MUST be in a subfolder for this to work!)
10. To start server, run `python manage.py runserver --settings=agdss.settings.[your settings]`.
11. The webapp can then be accessed at [http://localhost:8000](http://localhost:8000). For a list of available pages, see the file agdss/urls.py.


##Adding Images
Send a POST to /webclient/addImage with parameters:
  * `path`: location of image (not including image name itself. E.g. '/home/self/image-location/'). REQUIRED
  * `image-name`: name of image REQUIRED
  * `category`: Category of the image (e.g. 'apple'). REQUIRED
  * `description`: A description NOT REQUIRED
  * `source_description`: Description of image_source. NOT REQUIRED
Note that this POST request can be sent from anywhere. In the future it will require some method of authentication.

##TODO
1. Update paths to work from config file
2. Category selection menu rather than field in tagging page
