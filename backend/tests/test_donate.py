from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from apps.accounts.models import User
from apps.cases.models import Case, Category, Donation, Illustration


@pytest.mark.django_db
def test_donation_larger_than_balance_is_refused_and_nothing_changes():
    user = User.objects.create_user(email="donor@example.test", password="Pass-1234", name="Donor")
    wallet = user.wallet
    wallet.balance = Decimal("50.00")
    wallet.save()
    case = Case.objects.create(
        title="Test case",
        slug="test-case",
        summary="A case for the test.",
        story="Story.",
        category=Category.MEDICAL,
        city="Riyadh",
        goal=Decimal("1000.00"),
        illustration=Illustration.MEDICAL,
    )
    client = APIClient()
    client.force_authenticate(user)

    response = client.post(f"/api/cases/{case.slug}/donate/", {"amount": "100.00"}, format="json")

    assert response.status_code == 400
    assert response.json()["code"] == "insufficient_balance"
    wallet.refresh_from_db()
    case.refresh_from_db()
    assert wallet.balance == Decimal("50.00")
    assert case.raised == Decimal("0.00")
    assert case.donors_count == 0
    assert not Donation.objects.filter(case=case).exists()


@pytest.mark.django_db
def test_drill_deliberately_failing():
    assert Decimal("50.00") - Decimal("100.00") >= 0, "drill: this test fails on purpose"
