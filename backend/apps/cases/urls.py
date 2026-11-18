from django.urls import path

from . import views

urlpatterns = [
    path("cases/", views.CaseListView.as_view(), name="case-list"),
    path("cases/summary/", views.CaseSummaryView.as_view(), name="case-summary"),
    path("cases/<slug:slug>/", views.CaseDetailView.as_view(), name="case-detail"),
    path("cases/<slug:slug>/donate/", views.DonateView.as_view(), name="case-donate"),
    path("donations/<str:reference>/", views.ReceiptView.as_view(), name="donation-receipt"),
]
