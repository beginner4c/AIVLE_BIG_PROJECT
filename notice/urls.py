from django.urls import path
from. import views
app_name = 'notice'
urlpatterns = [
   path('list',views.notice_list, name='notice_list'),
   path('write',views.notice_write,name = "notice_write"),
   path('<int:pk>/', views.notice_detail, name='notice_detail'),
   path('<int:pk>/modify/', views.notice_modify, name='notice_modify'),
   path('<int:pk>/delete/', views.notice_delete, name='notice_delete'),
]