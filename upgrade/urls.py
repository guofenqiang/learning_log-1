from django.conf.urls import url
from . import views
from django.urls import path

urlpatterns = [
    url(r'^upgrade_home/$', views.upgrade_home, name='upgrade_home'),
    url(r'^line/$', views.ChartView.as_view(), name='line'),
    # url(r'^lineUpdate/$', views.ChartUpdateView.as_view(), name='lineUpdate'),
    url(r'^index/$', views.IndexView.as_view(), name='index'),
    # url(r'^index/$', views.index, name='index'),
    url(r'^reg/$', views.reg, name='reg'),
]