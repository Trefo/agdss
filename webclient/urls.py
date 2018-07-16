from django.conf.urls import url, include
from webclient import views as views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path


urlpatterns = [
                  #Page URLs
    path('', views.index, name='label_index'),
    path('label', views.label, name='label'),
    path('results', views.results, name='results'),
    path('view_label', views.view_label, name='view_label'),
    path('map_label', views.map_label, name='map_label'),

    #GET/POST URLs

    #path('purge$', views.purge),
    path('addImage', views.addImage),
    path('cleanUpAndFixImages', views.cleanUpAndFixImages),
    path('updateImage', views.updateImage),
    path('getInfo', views.getInfo),
    path('getNewImage', views.getNewImage),
    path('convertAll', views.convertAll),
    path('unlabeledImages', views.unlabeledImages),
    path('numImageLabels', views.numImageLabels),
    path('combineAllImages', views.combineAllImages),
    path('calculateEntropyMap', views.calculateEntropyMap),
    path('applyLabels', views.applyLabels),
    path('loadLabels', views.loadLabels),
    #path('fix_label_location', views.fix_label_location),
    path('print_label_data', views.print_label_data),
    url(r'^get_overlayed_combined_image/(?P<image_label_id>[0-9]*)$', views.get_overlayed_combined_image),
    url(r'^get_overlayed_category_image/(?P<category_label_id>[0-9]*)$', views.get_overlayed_category_image),
    path('addTiledLabel', views.add_tiled_label),
    path('TiledLables',views.get_all_tiled_labels),
    path('addTiledImage', views.add_train_image_label),
    path('addTiledCategories', views.add_all_tiled_categories),
    path('deleteTileLabels', views.delete_tile_label),
    path('getTiledLabelCoordinates', views.get_tiled_label_coordinates),
    path('getCombinedLabelGeojson', views.get_combined_label_geojson),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
