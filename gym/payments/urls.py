from django.urls import path, include
from .views import initiate_payment, verify_payment, subscribe
urlpatterns = [
    
    path('pay/', initiate_payment, name ='initiate_payment'),
    path('verify-payment/', verify_payment, name='verify_payment'),
    path('subscribe/', subscribe, name='subscribe')

    
]