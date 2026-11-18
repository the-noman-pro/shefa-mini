from decimal import Decimal

from django.conf import settings
from django.db import models


class Wallet(models.Model):
    """One per account. Money is always Decimal with two places, never float."""

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="wallet")
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.CheckConstraint(condition=models.Q(balance__gte=0), name="wallet_balance_not_negative"),
        ]

    def __str__(self):
        return f"Wallet of {self.user.email}: {self.balance} {settings.CURRENCY}"


class Transaction(models.Model):
    """The wallet ledger: every movement of money, with the balance right after it."""

    class Kind(models.TextChoices):
        TOP_UP = "top_up", "Top-up"
        DONATION = "donation", "Donation"

    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name="transactions")
    kind = models.CharField(max_length=16, choices=Kind.choices)
    # Positive for a top-up, negative for a donation.
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    balance_after = models.DecimalField(max_digits=12, decimal_places=2)
    reference = models.CharField(max_length=24, unique=True)
    description = models.CharField(max_length=200, blank=True)
    # Top-ups only. Brand and last four digits; the full number and CVV are never stored.
    card_brand = models.CharField(max_length=20, blank=True)
    card_last4 = models.CharField(max_length=4, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]
        indexes = [models.Index(fields=["wallet", "-created_at"])]

    def __str__(self):
        return f"{self.reference} {self.kind} {self.amount}"
