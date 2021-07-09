
from django.contrib import admin
from django.urls import path
from CChurn import views
urlpatterns = [
    path('Analysis',views.Analysis,name='Analysis'),
    path('form',views.Form,name='form'),
    path('form/upload',views.FormFileUpload,name='formUpload'),

]
