from django.urls import path

from . import views


app_name = "demo"


urlpatterns = [
    path("", views.Index.as_view(), name="index"),
    path(
        "signup/<int:source_id>/",
        views.ConsentCreateView.as_view(),
        name="signup",
    ),
    path(
        "signup/<int:source_id>/confirmation/",
        views.ConsentConfirmationSentView.as_view(),
        name="signup_confirmation",
    ),
]
