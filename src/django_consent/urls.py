from django.urls import path

from . import views


app_name = "consent"


urlpatterns = [
    path(
        "unsubscribe/<int:pk>/<str:token>/",
        views.UnsubscribeConsentView.as_view(),
        name="unsubscribe",
    ),
]
