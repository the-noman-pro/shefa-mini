from decimal import Decimal

from django.db import transaction as db_transaction
from rest_framework.exceptions import ValidationError

from apps.core.references import make_reference
from apps.wallets.models import Transaction, Wallet

from .models import Case, Donation

MIN_DONATION = Decimal("10.00")


def donate(user, case_id, amount, anonymous=False):
    """
    Move `amount` from the donor's wallet to an open case, all or nothing.

    Both rows are locked (SELECT ... FOR UPDATE) so two donations at the same moment cannot spend
    the same balance twice or push a case past its goal.
    """
    with db_transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(user=user)
        case = Case.objects.select_for_update().get(pk=case_id)

        if not case.is_open:
            raise ValidationError({"detail": "This case is no longer accepting donations."})
        if amount < MIN_DONATION:
            raise ValidationError({"amount": [f"The minimum donation is {MIN_DONATION:.0f} SAR."]})
        if amount > case.remaining:
            raise ValidationError(
                {"amount": [f"This case needs only {case.remaining:,.2f} SAR to reach its goal."]}
            )
        if amount > wallet.balance:
            raise ValidationError(
                {
                    "amount": [f"Your wallet has {wallet.balance:,.2f} SAR. Top up first."],
                    "code": "insufficient_balance",
                }
            )

        first_gift = not Donation.objects.filter(case=case, user=user).exists()

        wallet.balance -= amount
        wallet.save(update_fields=["balance", "updated_at"])

        reference = make_reference("DN")
        entry = Transaction.objects.create(
            wallet=wallet,
            kind=Transaction.Kind.DONATION,
            amount=-amount,
            balance_after=wallet.balance,
            reference=reference,
            description=f"Donation to {case.title}"[:200],
        )

        case.raised += amount
        if first_gift:
            case.donors_count += 1
        if case.raised >= case.goal:
            case.status = Case.Status.FUNDED
        case.save(update_fields=["raised", "donors_count", "status", "updated_at"])

        return Donation.objects.create(
            case=case,
            user=user,
            transaction=entry,
            amount=amount,
            anonymous=anonymous,
            display_name=user.public_name,
            reference=reference,
        )
