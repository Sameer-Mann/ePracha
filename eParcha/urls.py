from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name='home'),
    path('index/', views.index,name='index'),
    path('login/',views.login_user,name='login'),
    path('register/',views.register,name='register'),
    path('logout',views.logout_user,name='logout')
]