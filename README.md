# AgDSS
  Django based Agricultural Decision Support System (AgDSS) for robotic sampling in precision agriculture.
  Please note that this documentation is incomplete and may be out of date.


##Setup
1. git clone https://github.com/dcunhas/agdss
2. cd agdss
3. docker-compose up

##Additional steps needed in agdss web container, the first time for a composition
1. Run `python manage.py migrate --settings=agdss.settings.common` to create the tables in the database.
2. To create admin credentials (required to access /admin), run `python manage.py createsuperuser` and enter the requested information.
3. The webapp can then be accessed at [http://172.10.0.3:8000](http://172.10.0.3:8000). For a list of available pages, see the file agdss/urls.py.


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
