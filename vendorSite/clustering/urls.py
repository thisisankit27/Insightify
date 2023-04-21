from django.urls import path
from . import views

urlpatterns = [
    path('addBilling', views.addBilling, name='addBilling'),
    path('customerDatabase', views.customerDatabase, name='customerDatabase'),
]
