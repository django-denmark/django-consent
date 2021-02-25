from django.urls import path

from . import views

urlpatterns = [
    path(
        "unsubscribe/<int:source_id>/<str:email_hash>/<str:token>/",
        views.UnsubscribeConsentView.as_view(),
        name="unsubscribe",
    ),
]
