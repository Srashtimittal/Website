from django.urls import path
from . import views

urlpatterns = [
    path("", views.start, name="start"),
    path("elec/goods/<int:myid>", views.goodview, name="goodview"),
    path("elec/contact", views.contact, name="contact"),
    path("elec/register", views.register, name="register"),
    path("elec/login", views.login, name="login"),
    path("elec/logout", views.logout, name="logout"),
    path("elec/about", views.about, name="about"),
    path("elec/tracker", views.tracker, name="tracker"),
    path("elec/checkout", views.checkout, name="checkout"),
    path("elec/yui", views.yui, name="yui"),
    path("search/", views.search, name="search"),
    path("elec/handlerequest/", views.handlerequest, name="HandleRequest"),
]