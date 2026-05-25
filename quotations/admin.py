from django.contrib import admin

# Register your models here.



from .models import (
    Quotation,
    QuoteSection,
    QuoteItem
)


# =========================================
# QUOTE ITEM INLINE
# =========================================



from .models import Unit

admin.site.register(Unit)
class QuoteItemInline(admin.TabularInline):

    model = QuoteItem

    extra = 0

    fields = (
        "description",
        "quantity",
        "unit",
        "unit_price",
        "total_price",
        "sort_order"
    )

    readonly_fields = (
        "total_price",
    )


# =========================================
# QUOTE SECTION INLINE
# =========================================

class QuoteSectionInline(admin.StackedInline):

    model = QuoteSection

    extra = 0

    fields = (
        "title",
        "sort_order"
    )

    show_change_link = True


# =========================================
# QUOTE ITEM ADMIN
# =========================================

@admin.register(QuoteItem)
class QuoteItemAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "section",
        "quantity",
        "unit",
        "unit_price",
        "total_price",
        "sort_order"
    )

    list_filter = (
        "section",
    )

    search_fields = (
        "description",
        "section__title"
    )

    ordering = (
        "sort_order",
    )


# =========================================
# QUOTE SECTION ADMIN
# =========================================

@admin.register(QuoteSection)
class QuoteSectionAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "quotation",
        "title",
        "sort_order"
    )

    list_filter = (
        "quotation",
    )

    search_fields = (
        "title",
        "quotation__quote_number"
    )

    ordering = (
        "sort_order",
    )

    inlines = [
        QuoteItemInline
    ]


# =========================================
# QUOTATION ADMIN
# =========================================

@admin.register(Quotation)
class QuotationAdmin(admin.ModelAdmin):

    list_display = (
        "quote_number",
        "status",
        "submitted_to_name",
        "customer_phone",
        "subtotal",
        "vat_amount",
        "grand_total",
        "created_at"
    )

    list_filter = (
        "status",
        "created_at"
    )

    search_fields = (
        "quote_number",
        "submitted_to_name",
        "customer_phone",
        "customer_email",
        "reference_number"
    )

    ordering = (
        "-created_at",
    )

    readonly_fields = (
        "subtotal",
        "vat_amount",
        "grand_total",
        "created_at",
        "updated_at"
    )

    fieldsets = (

        (
            "Quotation Info",
            {
                "fields": (
                    "quote_number",
                    "status",
                    "reference_number",
                    "tag",
                    "material"
                )
            }
        ),

        (
            "Customer Info",
            {
                "fields": (
                    "submitted_to_name",
                    "submitted_to_details",
                    "customer_phone",
                    "customer_email"
                )
            }
        ),

        (
            "Submitted By",
            {
                "fields": (
                    "submitted_by_name",
                    "submitted_by_details",
                    "submitted_by_signature"
                )
            }
        ),

        (
            "Project Details",
            {
                "fields": (
                    "project_description",
                    "validity"
                )
            }
        ),

        (
            "Financial Details",
            {
                "fields": (
                    "vat_rate",
                    "warning_note",
                    "payment_terms",
                    "delivery_terms",
                    "included_items",
                    "excluded_items"
                )
            }
        ),

        (
            "Totals",
            {
                "fields": (
                    "subtotal",
                    "vat_amount",
                    "grand_total"
                )
            }
        ),

        (
            "Signatures & Dates",
            {
                "fields": (
                    "client_signature",
                    "created_at",
                    "updated_at"
                )
            }
        )

    )

    inlines = [
        QuoteSectionInline
    ]