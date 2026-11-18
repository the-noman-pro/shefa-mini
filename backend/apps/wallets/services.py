from django.db import transaction as db_transaction

from apps.core.references import make_reference

from .cards import DECLINED_TEST_CARD
from .models import Transaction, Wallet


class CardDeclined(Exception):
    pass


def simulate_processor(card_number):
    """Stand-in for a payment provider: one test card is always declined, any other valid card is approved."""
    if card_number == DECLINED_TEST_CARD:
        raise CardDeclined("Your bank declined this card. Try another card.")


def top_up(user, amount, card_number, brand):
    """Charge the (simulated) card, then credit the wallet. Only brand and last four are kept."""
    simulate_processor(card_number)
    with db_transaction.atomic():
        wallet = Wallet.objects.select_for_update().get(user=user)
        wallet.balance += amount
        wallet.save(update_fields=["balance", "updated_at"])
        return Transaction.objects.create(
            wallet=wallet,
            kind=Transaction.Kind.TOP_UP,
            amount=amount,
            balance_after=wallet.balance,
            reference=make_reference("TP"),
            description="Wallet top-up",
            card_brand=brand,
            card_last4=card_number[-4:],
        )
