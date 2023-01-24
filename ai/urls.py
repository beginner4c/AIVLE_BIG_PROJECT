from django.urls import path
from . import views
app_name = 'ai'
urlpatterns = [
   path('result',views.result, name='result'),
   path('info',views.info, name = 'info'),
   path('db_upload',views.db_upload,name = 'db_upload'),
   
]