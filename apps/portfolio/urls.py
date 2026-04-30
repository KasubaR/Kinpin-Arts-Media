from django.urls import path
from . import views

urlpatterns = [
    path('', views.portfolio_list, name='portfolio'),
    path('<slug:slug>/', views.portfolio_detail, name='portfolio_detail'),
]
