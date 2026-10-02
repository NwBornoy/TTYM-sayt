from django.urls import path
from . import views

urlpatterns = [
    path("telegram/webhook/<str:secret>/", views.webhook),
]