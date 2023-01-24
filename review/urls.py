from django.urls import path
from . import views
app_name = 'review'
urlpatterns = [
   path('list',views.review_list, name='review_list'),
   path('write',views.review_write,name = "review_write"),
   path('<int:pk>/', views.review_detail, name='review_detail'),
   path('<int:pk>/modify/', views.review_modify, name='review_modify'),
   path('<int:pk>/delete/', views.review_delete, name='review_delete'),
]