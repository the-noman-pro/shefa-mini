from decimal import Decimal

from django.conf import settings
from django.db import models


class Category(models.TextChoices):
    MEDICAL = "medical", "Medical"
    EDUCATION = "education", "Education"
    HOUSING = "housing", "Housing"
    FOOD = "food", "Food"
    WATER = "water", "Water"
    DEBT = "debt", "Debt relief"


class Illustration(models.TextChoices):
    """Keys of the hand-drawn SVGs the frontend ships (frontend/src/components/art/)."""

    MEDICAL = "medical", "Stethoscope and heart"
    EDUCATION = "education", "School bag and books"
    HOUSING = "housing", "House and key"
    FOOD = "food", "Food basket"
    WATER = "water", "Water well"
    DEBT = "debt", "Open hands and coins"


class Case(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        FUNDED = "funded", "Funded"
        CLOSED = "closed", "Closed"

    title = models.CharField(max_length=140)
    slug = models.SlugField(max_length=160, unique=True)
    summary = models.CharField(max_length=220, help_text="One or two lines for the case card.")
    story = models.TextField(help_text="Paragraphs separated by a blank line.")
    category = models.CharField(max_length=20, choices=Category.choices)
    city = models.CharField("beneficiary city", max_length=60)
    goal = models.DecimalField(max_digits=12, decimal_places=2)
    raised = models.DecimalField(max_digits=12, decimal_places=2, default=Decimal("0.00"))
    donors_count = models.PositiveIntegerField(default=0)
    illustration = models.CharField(max_length=20, choices=Illustration.choices)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.OPEN)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["status", "-created_at"]
        constraints = [
            models.CheckConstraint(condition=models.Q(goal__gt=0), name="case_goal_positive"),
            models.CheckConstraint(condition=models.Q(raised__gte=0), name="case_raised_not_negative"),
        ]

    def __str__(self):
        return self.title

    @property
    def remaining(self):
        return max(self.goal - self.raised, Decimal("0.00"))

    @property
    def is_open(self):
        return self.status == self.Status.OPEN


class Donation(models.Model):
    case = models.ForeignKey(Case, on_delete=models.PROTECT, related_name="donations")
    # Empty for seeded sample donations.
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="donations",
    )
    transaction = models.OneToOneField(
        "wallets.Transaction",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="donation",
    )
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    anonymous = models.BooleanField(default=False)
    # Name shown in "recent donations", fixed at donation time.
    display_name = models.CharField(max_length=60)
    reference = models.CharField(max_length=24, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at", "-id"]

    def __str__(self):
        return f"{self.reference} {self.amount} to {self.case}"

    @property
    def public_name(self):
        return "Anonymous" if self.anonymous else self.display_name
