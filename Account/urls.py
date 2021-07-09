
from django.contrib import admin
from django.urls import path
from Account import views
urlpatterns = [
    path('dash',views.dash,name='dash'),
    path('signup',views.signup,name='signup'),
    path('logout',views.logout,name='logout'),

]
