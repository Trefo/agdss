# AgDSS
  Django based Agricultural Decision Support System (AgDSS) for robotic sampling in precision agriculture.
  Please note that this documentation is incomplete and may be out of date.


##Setup
1. git clone https://github.com/Trefo/agdss
2. cd agdss
3. docker-compose up  

## First-time additional steps needed in agdss web container named agdss_web 
You need to edit /app/agdss/settings/common.py specifying correctly the image category you want to label, and the label folder name. Then, run the following commands. 
1. ```docker exec -it agdss_web_1 bash```
2. ```python manage.py migrate --settings=agdss.settings.common``` to create the tables in the database.
3. ```python manage.py createsuperuser --settings=agdss.settings.common``` and enter the requested information.
4. ```python manage.py collectstatic --settings=agdss.settings.common ```
5. ```cp /app/addImages.sh  /app/static-root/small-tomatoes && cd /app/static-root/small-tomatoes/```
6. ```bash addImages.sh "[\"small-tomatoes\"]" ```

## Using the aannotation webapp 
The webapp can then be accessed at [http://172.10.0.3:8000](http://172.10.0.3:8000). 

Admin page is at [http://172.10.0.3:8000/admin](http://172.10.0.3:8000/admin)
Use the credential you created for the superuser in item 3. for first-time additional steps.  

For a list of available pages, see the file agdss/urls.py

## Viewing labels 
Labels are stored in the folder specified in the settings file, default being 'labels', which should be in the static-root folder. Labels can also be inspected through the web app using the admin image labels page. 
