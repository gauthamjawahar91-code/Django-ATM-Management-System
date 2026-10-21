from django.urls import path
from . import views

urlpatterns = [
    path('deposit/',views.deposit,name='deposit'),
    path('withdraw/',views.withdraw , name='withdraw'),
    path('transfer/',views.transfer,name='transfer'),
    path('statement/',views.statement,name='statement'),
    path('mini_statement/',views.mini_statement,name='mini_statement')
]