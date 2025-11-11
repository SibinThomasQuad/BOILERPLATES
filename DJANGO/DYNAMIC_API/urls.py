from django.urls import path
from . import views

urlpatterns = [
    path('api/dynamic_api/<str:table>/<str:type>/', views.dynamic_api, name='dynamic_api'),
]
