from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('home/', views.home_view, name='home'),
    path('raum1/', views.raum1_view, name='raum1'),
    path('raum2/', views.raum2_view, name='raum2'),
    path('raum3/', views.raum3_view, name='raum3'),
    path('raum4/', views.raum4_view, name='raum4')
    
]