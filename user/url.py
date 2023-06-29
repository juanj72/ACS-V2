from django.urls import path
from user.views import *

urlpatterns = [
  
    path('',index,name='inicio'),
    path('confirmacion/<id>',confirmacionventa,name='okventa'),
  
]
