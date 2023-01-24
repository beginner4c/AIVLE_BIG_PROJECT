from django.urls import path
from . import views
app_name = 'user'
urlpatterns = [    
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path('main/', views.main, name='main'),
    path("login/", views.my_login, name="login"),
    path('logout/',views.log_out, name = 'logout'),
    path("verify/<str:key>", views.complete_verification, name="complete-verification"),
    path('mypage/',views.mypage,name = 'mypage'),
    path('traivler',views.traivler,name = 'traivler'),
    
]