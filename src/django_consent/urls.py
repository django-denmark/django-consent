from django.urls import path

from . import views


app_name = "consent"


urlpatterns = [
    path(
        "subscribe/<int:pk>/<str:token>/",
        views.SubscribeConsentConfirmView.as_view(),
        name="consent_confirm",
    ),
    path(
        "unsubscribe/<int:pk>/<str:token>/",
        views.UnsubscribeConsentView.as_view(),
        name="unsubscribe",
    ),
    path(
        "unsubscribe/<int:pk>/<str:token>/undo/",
        views.UnsubscribeConsentUndoView.as_view(),
        name="unsubscribe_undo",
    ),
]
