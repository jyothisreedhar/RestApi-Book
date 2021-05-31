
from django.contrib import admin
from django.urls import path
from .views import book_list,book_details,BookListView,BookDetailView,BookMixinView,BookDetailMixinView,LoginApi


urlpatterns = [
    path("list",book_list,name="list"),
    path("details/<int:id>",book_details,name="details"),
    path("clist",BookListView.as_view(),name="clist"),
    path("cdetails/<int:id>",BookDetailView.as_view(),name="cdetails"),
    path("mlist",BookMixinView.as_view(),name="mlist"),
    path("mdetails/<int:pk>",BookDetailMixinView.as_view(),name="mdetails"),
    path("login",LoginApi.as_view(),name="login")
]
