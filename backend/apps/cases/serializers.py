from decimal import Decimal

from rest_framework import serializers

from apps.wallets.cards import parse_amount

from .models import Case, Donation
from .services import MIN_DONATION


class CaseListSerializer(serializers.ModelSerializer):
    category_label = serializers.CharField(source="get_category_display", read_only=True)
    remaining = serializers.DecimalField(max_digits=12, decimal_places=2, read_only=True)

    class Meta:
        model = Case
        fields = [
            "id",
            "slug",
            "title",
            "summary",
            "category",
            "category_label",
            "city",
            "goal",
            "raised",
            "remaining",
            "donors_count",
            "illustration",
            "status",
        ]


class RecentDonationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="public_name")

    class Meta:
        model = Donation
        fields = ["name", "amount", "created_at"]


class CaseDetailSerializer(CaseListSerializer):
    recent_donations = serializers.SerializerMethodField()

    class Meta(CaseListSerializer.Meta):
        fields = CaseListSerializer.Meta.fields + ["story", "created_at", "recent_donations"]

    def get_recent_donations(self, obj):
        return RecentDonationSerializer(obj.donations.all()[:8], many=True).data


class DonateSerializer(serializers.Serializer):
    amount = serializers.CharField(max_length=16)
    anonymous = serializers.BooleanField(default=False)

    def validate_amount(self, value):
        amount, error = parse_amount(value, minimum=MIN_DONATION, maximum=Decimal("1000000"))
        if error:
            raise serializers.ValidationError(error)
        return amount


class ReceiptSerializer(serializers.ModelSerializer):
    case = serializers.SerializerMethodField()
    balance_after = serializers.DecimalField(
        source="transaction.balance_after", max_digits=12, decimal_places=2, read_only=True
    )
    donor_name = serializers.CharField(source="display_name")

    class Meta:
        model = Donation
        fields = [
            "reference",
            "amount",
            "anonymous",
            "donor_name",
            "case",
            "balance_after",
            "created_at",
        ]

    def get_case(self, obj):
        case = obj.case
        return {
            "slug": case.slug,
            "title": case.title,
            "city": case.city,
            "category": case.category,
            "illustration": case.illustration,
            "goal": str(case.goal),
            "raised": str(case.raised),
            "donors_count": case.donors_count,
            "status": case.status,
        }
