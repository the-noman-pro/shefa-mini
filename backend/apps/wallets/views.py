from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.throttling import ScopedRateThrottle
from rest_framework.views import APIView

from .serializers import TopUpSerializer, TransactionSerializer, WalletSerializer
from .services import CardDeclined, top_up


class WalletView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(WalletSerializer(request.user.wallet).data)


class TransactionListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = TransactionSerializer

    def get_queryset(self):
        return self.request.user.wallet.transactions.select_related("donation__case")


@method_decorator(sensitive_post_parameters("card_number", "cvv", "expiry"), name="dispatch")
class TopUpView(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = "top_up"

    def post(self, request):
        serializer = TopUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            entry = top_up(request.user, data["amount"], data["card_number"], data["brand"])
        except CardDeclined as exc:
            return Response(
                {"status": "declined", "code": "card_declined", "detail": str(exc)},
                status=status.HTTP_402_PAYMENT_REQUIRED,
            )
        return Response(
            {
                "status": "approved",
                "transaction": TransactionSerializer(entry).data,
                "balance": str(entry.balance_after),
            },
            status=status.HTTP_201_CREATED,
        )
