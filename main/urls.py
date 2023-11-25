from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("xsscan/", views.xsscan, name="xsscan"),
    path("targets/", views.targets, name="targets"),
    path("results/", views.results, name="results"),
    path("targets/<int:id>", views.target_info, name="target_info"),
]