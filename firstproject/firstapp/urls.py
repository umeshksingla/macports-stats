from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('port/<int:port_id>/', views.detail, name='detail'),
    path('submission', views.get_submissions, name='submissions'),
    path('portindex', views.get_portindex, name='portindex'),
]
