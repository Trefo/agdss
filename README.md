# AgDSS
  Django based Agricultural Decision Support System (AgDSS) for robotic sampling in precision agriculture.
  Please note that this documentation is incomplete and may be out of date.


## Setup
The folder annotable/small-tomatoes has a set of example images. Accordingly, the /app/agdss/settings/common.py file assumes small-tomatoes as category. You need to specify your own folder and image category you want to label, as well as the name of folders where converted label masks will be stored (degault 'labels/'). Run the following commands once satisfied with the settings file. 

1. git clone https://github.com/Trefo/agdss
2. cd agdss
3. docker-compose up  

## First-time additional steps needed in agdss web container named agdss_web 
On a different terminal. 
1. ```docker exec -it agdss_web_1 bash```
2. ```python manage.py migrate --settings=agdss.settings.common``` to create the tables in the database.
3. ```python manage.py createsuperuser --settings=agdss.settings.common``` and enter the requested information.
4. ```python manage.py collectstatic --settings=agdss.settings.common ```
5. ```cp /app/addImages.sh  /app/static-root/small-tomatoes```
6. ```cd /app/static-root/small-tomatoes/```
7. ```bash addImages.sh "[\"small-tomatoes\"]" ```

## On using the annotation web app 
The web app can then be accessed at [http://172.10.0.3:8000](http://172.10.0.3:8000). 

Admin page is at [http://172.10.0.3:8000/admin](http://172.10.0.3:8000/admin)
Use the credential you created for the superuser in item 3. for first-time additional steps.  

For a list of available pages, see the file agdss/urls.py

## Viewing labels 
Labels are stored in the folder specified in the settings file, default being 'labels', which should be in the static-root folder. Labels can also be inspected through the web app using the admin image labels page. 

## UI Controls 
You can resize the browser using standard browser controls (Ctrl+ and Ctrl-). Additionally, the app has sliders to control brightness, contrast, and hue. Adjust these to make the target objects clearer.

Labels can be moved by dragging, and deleted by double-clicking.

Submit when finished labeling an image. 

Chose 'No labels in image' when there are no labels so that that the data is recorded correctly on the DB. 
