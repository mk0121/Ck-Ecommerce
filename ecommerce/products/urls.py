from django.urls import path
from . import views

urlpatterns = [
    path('products', views.PoductView.as_view()),
    path('demo', views.DemoView.as_view()),
]
