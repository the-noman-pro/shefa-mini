import re

from django.conf import settings
from rest_framework import serializers

from . import cards
from .models import Transaction, Wallet


class WalletSerializer(serializers.ModelSerializer):
    currency = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        fields = ["balance", "currency", "updated_at"]

    def get_currency(self, obj):
        return settings.CURRENCY


class TransactionSerializer(serializers.ModelSerializer):
    case = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = [
            "id",
            "kind",
            "amount",
            "balance_after",
            "reference",
            "description",
            "card_brand",
            "card_last4",
            "case",
            "created_at",
        ]

    def get_case(self, obj):
        donation = getattr(obj, "donation", None)
        if donation is None:
            return None
        return {"slug": donation.case.slug, "title": donation.case.title}


class TopUpSerializer(serializers.Serializer):
    """Validates the dummy card. Values are used once and never saved or logged."""

    card_holder = serializers.CharField(max_length=60)
    card_number = serializers.CharField(max_length=32, trim_whitespace=True)
    expiry = serializers.CharField(max_length=7)
    cvv = serializers.CharField(max_length=4, trim_whitespace=True)
    amount = serializers.CharField(max_length=16)

    def validate_card_holder(self, value):
        value = " ".join(value.split())
        if len(value) < 2 or not re.fullmatch(r"[A-Za-z][A-Za-z .'\-]*", value):
            raise serializers.ValidationError("Enter the name as printed on the card.")
        return value

    def validate_amount(self, value):
        amount, error = cards.parse_amount(value)
        if error:
            raise serializers.ValidationError(error)
        return amount

    def to_internal_value(self, data):
        # Collect every problem in one response, so the form can mark all bad fields at once.
        errors = {}
        try:
            attrs = super().to_internal_value(data)
        except serializers.ValidationError as exc:
            errors.update(exc.detail)
            attrs = {}
        raw = data if hasattr(data, "get") else {}

        number, brand, error = cards.validate_card_number(str(raw.get("card_number") or ""))
        if error and "card_number" not in errors:
            errors["card_number"] = [error]
        _, _, error = cards.parse_expiry(str(raw.get("expiry") or ""))
        if error and "expiry" not in errors:
            errors["expiry"] = [error]
        error = cards.validate_cvv(str(raw.get("cvv") or "").strip(), brand)
        if error and "cvv" not in errors:
            errors["cvv"] = [error]

        if errors:
            raise serializers.ValidationError(errors)
        attrs["card_number"] = number
        attrs["brand"] = brand
        return attrs
