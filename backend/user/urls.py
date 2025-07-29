from django.urls import path
from . import views

urlpatterns = [
    # Basic hello endpoint
    path('hello/', views.HelloView.as_view(), name='hello'),
]
