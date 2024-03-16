from django.urls import path, include, re_path
from . import views

urlpatterns = [
    path('mainapp/', include('mainapp.urls')),
    re_path(r'^$', views.ticket_list)
]
