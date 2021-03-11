from django.urls import path

from . import views


app_name = "consent"


urlpatterns = [
    path(
        "subscribe/<int:pk>/<str:token>/",
        views.ConsentConfirmationReceiveView.as_view(),
        name="consent_confirm",
    ),
    path(
        "unsubscribe/<int:pk>/<str:token>/",
        views.ConsentWithdrawView.as_view(),
        name="unsubscribe",
    ),
    path(
        "unsubscribe/<int:pk>/<str:token>/undo/",
        views.ConsentWithdrawUndoView.as_view(),
        name="unsubscribe_undo",
    ),
]
