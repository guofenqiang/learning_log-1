from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    url(r'^line/$', views.ChartView.as_view(), name='demo'),
    url(r'^lineUpdate/$', views.ChartUpdateView.as_view(), name='demo'),
    url(r'^index/$', views.IndexView.as_view(), name='demo'),
    url(r'^reg/$', views.reg, name='demo'),
]