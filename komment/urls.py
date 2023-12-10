from django.urls import path

from . import views

urlpatterns = [
    path("usaco/<str:ch>/<str:prog>/comment", views.UsacoCommentView.as_view(), name="usaco_comments"),
    path("usaco/<str:ch>/<str:prog>/raw", views.UsacoGithubCodeView.as_view(), name="usaco_code_raw"),
]