from django.urls import path

from . import views

urlpatterns = [
    path("usaco/<str:ch>/<str:prog>/comment", views.usaco_comments, name="usaco_comments"),
    path("usaco/<str:ch>/<str:prog>/raw", views.usaco_code_raw, name="usaco_code_raw"),
]