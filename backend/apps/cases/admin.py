from django.contrib import admin

from .models import Case, Donation


class DonationInline(admin.TabularInline):
    model = Donation
    extra = 0
    can_delete = False
    fields = ["created_at", "display_name", "anonymous", "amount", "reference"]
    readonly_fields = fields
    ordering = ["-created_at"]

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Case)
class CaseAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "city", "goal", "raised", "donors_count", "status"]
    list_filter = ["status", "category", "city"]
    search_fields = ["title", "summary", "city"]
    prepopulated_fields = {"slug": ["title"]}
    readonly_fields = ["created_at", "updated_at"]
    fieldsets = (
        (None, {"fields": ("title", "slug", "summary", "story")}),
        ("Where and what", {"fields": ("category", "city", "illustration")}),
        ("Funding", {"fields": ("goal", "raised", "donors_count", "status")}),
        ("Dates", {"fields": ("created_at", "updated_at")}),
    )
    inlines = [DonationInline]


@admin.register(Donation)
class DonationAdmin(admin.ModelAdmin):
    list_display = ["reference", "case", "display_name", "anonymous", "amount", "created_at"]
    list_filter = ["anonymous", "case__category"]
    search_fields = ["reference", "display_name", "user__email", "case__title"]
    readonly_fields = [f.name for f in Donation._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False
