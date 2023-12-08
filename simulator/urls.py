from django.urls import path
from simulator import views

urlpatterns = [
    path("", views.index, name="index"),
    path("list/", views.ListItemCartView.as_view(), name="list_item"),
]