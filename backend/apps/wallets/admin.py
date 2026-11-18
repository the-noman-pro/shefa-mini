from django.contrib import admin

from .models import Transaction, Wallet


class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0
    can_delete = False
    fields = ["created_at", "kind", "amount", "balance_after", "reference", "card_brand", "card_last4"]
    readonly_fields = fields
    ordering = ["-created_at"]

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ["user", "balance", "updated_at"]
    search_fields = ["user__email", "user__name"]
    readonly_fields = ["user", "balance", "created_at", "updated_at"]
    inlines = [TransactionInline]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ["reference", "kind", "amount", "balance_after", "wallet", "created_at"]
    list_filter = ["kind"]
    search_fields = ["reference", "wallet__user__email"]
    readonly_fields = [f.name for f in Transaction._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
