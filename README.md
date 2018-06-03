# AgDSS
  Django based Agricultural Decision Support System (AgDSS) for robotic sampling in precision agriculture.
  Please note that this documentation is incomplete and may be out of date.


##Setup
1. git clone https://github.com/dcunhas/agdss
2. cd agdss
3. docker-compose up

##Additional steps needed in agdss web container, the first time for a composition
0. docker exec -it agdss_web_1 bash
1. Run `python manage.py migrate --settings=agdss.settings.common` to create the tables in the database.
2. To create admin credentials (required to access /admin), run `python manage.py createsuperuser` and enter the requested information.
3. The webapp can then be accessed at [http://172.10.0.3:8000](http://172.10.0.3:8000). For a list of available pages, see the file agdss/urls.py.
4. python manage.py collectstatic --settings=agdss.settings.common 
5. Copy addImages.sh to static-root/<your-image-folder>
6. bash addImages.sh "\"category-name"\"
