from django.urls import path

from . import views

urlpatterns = [
    path("", views.WalletView.as_view(), name="wallet"),
    path("transactions/", views.TransactionListView.as_view(), name="wallet-transactions"),
    path("top-up/", views.TopUpView.as_view(), name="wallet-top-up"),
]
