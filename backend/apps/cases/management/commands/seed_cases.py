from decimal import Decimal

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.core.references import make_reference
from apps.wallets.models import Transaction, Wallet

from ...models import Case, Donation

# Names and places are illustrative; no case describes a real person.
CASES = [
    {
        "slug": "dialysis-for-umm-khalid",
        "title": "Three dialysis sessions a week for Umm Khalid",
        "summary": "A grandmother in Hail needs her kidney treatment covered for the next six months.",
        "story": (
            "Umm Khalid is 64 and lives with her son's family on the edge of Hail. Since her kidneys "
            "failed last spring she travels to the city hospital three times a week for dialysis.\n\n"
            "Her son drives a school bus and his salary covers rent and food for seven people. The "
            "treatment itself is partly covered, but transport, medication and the sessions not on her "
            "plan add up to more than the family earns in a month.\n\n"
            "Your gift pays for six months of sessions and the medication between them, so she can keep "
            "treatment going while her transplant application is reviewed."
        ),
        "category": "medical",
        "city": "Hail",
        "goal": "42000.00",
        "raised": "27850.00",
        "donors_count": 214,
        "illustration": "medical",
        "donors": [
            ("Faisal M.", "500.00", False),
            ("Anonymous", "150.00", True),
            ("Reem S.", "100.00", False),
        ],
    },
    {
        "slug": "school-year-for-four-siblings",
        "title": "A full school year for four siblings",
        "summary": "Uniforms, books, transport and fees for four children whose father passed away in May.",
        "story": (
            "Four brothers and sisters, aged 7 to 15, lost their father in May. Their mother works "
            "part-time at a tailoring shop in Jeddah and wants the children to stay in the school they "
            "know.\n\n"
            "The school has waived part of the fees. What remains is the rest of the tuition, uniforms, "
            "books, tablets for the two older children and the school bus for the year.\n\n"
            "Every 250 SAR covers one child's books and uniform for a term."
        ),
        "category": "education",
        "city": "Jeddah",
        "goal": "18500.00",
        "raised": "11240.00",
        "donors_count": 96,
        "illustration": "education",
        "donors": [("Noura A.", "250.00", False), ("Omar H.", "250.00", False), ("Anonymous", "50.00", True)],
    },
    {
        "slug": "safe-roof-before-winter",
        "title": "A safe roof before winter in Abha",
        "summary": "A family of six is living under a leaking roof that could give way in the rains.",
        "story": (
            "The house was built by the grandfather forty years ago. Last season's rains soaked through "
            "the roof beams, and an engineer from the municipality has marked two rooms unsafe.\n\n"
            "The family now sleeps in one room. A local contractor has quoted the repair: new beams, "
            "a sealed concrete roof and gutters that carry the water away from the walls.\n\n"
            "The work takes three weeks once funded, and must finish before the heavy rains in the "
            "mountains."
        ),
        "category": "housing",
        "city": "Abha",
        "goal": "36000.00",
        "raised": "9300.00",
        "donors_count": 58,
        "illustration": "housing",
        "donors": [("Sultan K.", "1000.00", False), ("Anonymous", "200.00", True)],
    },
    {
        "slug": "monthly-food-baskets-dammam",
        "title": "Monthly food baskets for 40 families",
        "summary": "Rice, oil, flour, dates and lentils delivered each month to families in east Dammam.",
        "story": (
            "A neighbourhood group in east Dammam has delivered food baskets for three years. Most of "
            "the families are elderly couples or widows with young children.\n\n"
            "Each basket feeds a family for about a month: rice, flour, cooking oil, lentils, sugar, tea, "
            "milk powder and a box of dates. The group buys in bulk from a wholesaler to keep each basket "
            "under 180 SAR.\n\n"
            "This round covers three months of baskets for 40 families."
        ),
        "category": "food",
        "city": "Dammam",
        "goal": "21600.00",
        "raised": "17920.00",
        "donors_count": 303,
        "illustration": "food",
        "donors": [("Huda R.", "180.00", False), ("Anonymous", "360.00", True), ("Majed T.", "90.00", False)],
    },
    {
        "slug": "water-tank-for-village-school",
        "title": "Clean water for a village school near Tabuk",
        "summary": "A storage tank and filter so 120 pupils have safe drinking water all day.",
        "story": (
            "The primary school in a village outside Tabuk gets its water by truck once a week. The old "
            "tank is rusted inside, and by Thursday the water is not safe to drink.\n\n"
            "The plan is a new insulated tank, a filter unit, and four drinking taps in the yard. The "
            "parents' committee will look after the filters, and the teachers have arranged the delivery "
            "schedule with the municipality.\n\n"
            "Once installed it serves 120 pupils and their teachers every school day."
        ),
        "category": "water",
        "city": "Tabuk",
        "goal": "14800.00",
        "raised": "4150.00",
        "donors_count": 37,
        "illustration": "water",
        "donors": [("Abdullah F.", "300.00", False), ("Lama J.", "100.00", False)],
    },
    {
        "slug": "rent-arrears-madinah",
        "title": "Clear the rent arrears of a father in Madinah",
        "summary": "Seven months of unpaid rent after a work injury; the family faces eviction in January.",
        "story": (
            "A father of three injured his back at a construction site in March and could not work for "
            "most of the year. The family fell seven months behind on rent.\n\n"
            "He has started light work again and can keep up with rent from now on, but the arrears are "
            "beyond him. The landlord has agreed to stop the eviction if the balance is paid by the end "
            "of December.\n\n"
            "The amount is paid directly to the landlord against a receipt."
        ),
        "category": "debt",
        "city": "Madinah",
        "goal": "15400.00",
        "raised": "6020.00",
        "donors_count": 44,
        "illustration": "debt",
        "donors": [("Anonymous", "500.00", True), ("Yousef B.", "120.00", False)],
    },
    {
        "slug": "wheelchair-for-salem",
        "title": "A powered wheelchair for a university student",
        "summary": "Funded: a student in Riyadh can now reach his lectures on his own.",
        "story": (
            "A 20-year-old engineering student in Riyadh lives with muscular dystrophy. His manual chair "
            "meant he depended on classmates to move between buildings.\n\n"
            "Donors covered a powered wheelchair fitted to his measurements, with a spare battery. He "
            "picked it up in October and now gets to every lecture on his own.\n\n"
            "Thank you to everyone who gave."
        ),
        "category": "medical",
        "city": "Riyadh",
        "goal": "24000.00",
        "raised": "24000.00",
        "donors_count": 187,
        "illustration": "medical",
        "status": "funded",
        "donors": [("Maha Q.", "400.00", False), ("Anonymous", "1000.00", True)],
    },
]

DEMO_EMAIL = "demo@shefa-mini.test"
DEMO_PASSWORD = "GiveWell2026"
DEMO_NAME = "Sara Alharbi"
DEMO_BALANCE = Decimal("500.00")


class Command(BaseCommand):
    help = "Create the sample cases (safe to run again: existing cases are left as they are)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--demo-user",
            action="store_true",
            help=f"Also create {DEMO_EMAIL} with a {DEMO_BALANCE} SAR wallet.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        created = 0
        # Newest first on the cases page, so create in reverse to show them in the order listed.
        for data in reversed(CASES):
            data = dict(data)
            donors = data.pop("donors")
            slug = data.pop("slug")
            for money in ("goal", "raised"):
                data[money] = Decimal(data[money])
            case, was_created = Case.objects.get_or_create(slug=slug, defaults=data)
            if was_created:
                created += 1
                for name, amount, anonymous in donors:
                    Donation.objects.create(
                        case=case,
                        amount=Decimal(amount),
                        anonymous=anonymous,
                        display_name="A donor" if anonymous else name,
                        reference=make_reference("DN"),
                    )
        self.stdout.write(
            self.style.SUCCESS(f"Cases: {created} created, {len(CASES) - created} already there.")
        )
        if options["demo_user"]:
            self._demo_user()

    def _demo_user(self):
        User = get_user_model()
        user = User.objects.filter(email=DEMO_EMAIL).first()
        if user:
            self.stdout.write(f"Demo user {DEMO_EMAIL} already there.")
            return
        user = User.objects.create_user(email=DEMO_EMAIL, password=DEMO_PASSWORD, name=DEMO_NAME)
        wallet = Wallet.objects.select_for_update().get(user=user)
        wallet.balance = DEMO_BALANCE
        wallet.save(update_fields=["balance", "updated_at"])
        Transaction.objects.create(
            wallet=wallet,
            kind=Transaction.Kind.TOP_UP,
            amount=DEMO_BALANCE,
            balance_after=DEMO_BALANCE,
            reference=make_reference("TP"),
            description="Wallet top-up",
            card_brand="visa",
            card_last4="4242",
        )
        self.stdout.write(
            self.style.SUCCESS(f"Demo user: {DEMO_EMAIL} / {DEMO_PASSWORD} ({DEMO_BALANCE} SAR)")
        )
