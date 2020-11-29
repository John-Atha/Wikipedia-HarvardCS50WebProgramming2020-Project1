from django.urls import path

from . import views

app_name="encyclopedia"
urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title1>", views.display, name="display"),
    path("add", views.add, name="add"),
    path("encyclopedia/results_page.html", views.search, name="search"),
    path("random_page", views.random_page, name="random"),
    path("edit/", views.edit, name="edit"),
    path("save/", views.save, name="save")
]
