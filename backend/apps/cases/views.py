from decimal import Decimal

from django.db import models
from django.db.models import Count, Q, Sum
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Case, Category, Donation
from .serializers import (
    CaseDetailSerializer,
    CaseListSerializer,
    DonateSerializer,
    ReceiptSerializer,
)
from .services import donate


class CaseListView(generics.ListAPIView):
    """All cases, open first. Filters: ?category=medical  ?status=open"""

    permission_classes = [AllowAny]
    serializer_class = CaseListSerializer
    pagination_class = None

    def get_queryset(self):
        queryset = Case.objects.annotate(
            closed_rank=models.Case(
                models.When(status=Case.Status.OPEN, then=0), default=1, output_field=models.IntegerField()
            )
        ).order_by("closed_rank", "-created_at", "-id")
        category = self.request.query_params.get("category")
        if category:
            queryset = queryset.filter(category=category)
        case_status = self.request.query_params.get("status")
        if case_status:
            queryset = queryset.filter(status=case_status)
        return queryset


class CaseSummaryView(APIView):
    """Totals for the cases page header plus the categories that have cases, with counts."""

    permission_classes = [AllowAny]

    def get(self, request):
        totals = Case.objects.aggregate(
            raised=Sum("raised"),
            donors=Sum("donors_count"),
            funded=Count("id", filter=Q(status=Case.Status.FUNDED)),
            open=Count("id", filter=Q(status=Case.Status.OPEN)),
        )
        counts = dict(
            Case.objects.values_list("category").annotate(n=Count("id")).values_list("category", "n")
        )
        categories = [
            {"key": key, "label": label, "count": counts[key]}
            for key, label in Category.choices
            if counts.get(key)
        ]
        return Response(
            {
                "raised": f"{totals['raised'] or Decimal(0):.2f}",
                "donors": totals["donors"] or 0,
                "funded": totals["funded"],
                "open": totals["open"],
                "categories": categories,
            }
        )


class CaseDetailView(generics.RetrieveAPIView):
    permission_classes = [AllowAny]
    serializer_class = CaseDetailSerializer
    queryset = Case.objects.all()
    lookup_field = "slug"


class DonateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, slug):
        case = get_object_or_404(Case, slug=slug)
        serializer = DonateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        donation = donate(
            request.user,
            case.pk,
            serializer.validated_data["amount"],
            anonymous=serializer.validated_data["anonymous"],
        )
        return Response(ReceiptSerializer(donation).data, status=status.HTTP_201_CREATED)


class ReceiptView(generics.RetrieveAPIView):
    """A donor's own receipt, by reference. Other people's receipts answer 404."""

    permission_classes = [IsAuthenticated]
    serializer_class = ReceiptSerializer
    lookup_field = "reference"

    def get_queryset(self):
        return Donation.objects.filter(user=self.request.user).select_related("case", "transaction")
