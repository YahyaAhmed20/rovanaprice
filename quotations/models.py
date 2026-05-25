from django.db import models


# =========================================
# QUOTATION
# =========================================

class Quotation(models.Model):

    STATUS_CHOICES = [

    ("draft", "Draft"),

    ("sent", "Sent"),

    ("approved", "Approved"),

    ("rejected", "Rejected")

]
    quote_number = models.CharField(
        max_length=50,
        unique=True
    )
    status = models.CharField(
    max_length=20,
    choices=STATUS_CHOICES,
    default="draft"
    )

    reference_number = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    tag = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    material = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    customer_phone = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    customer_email = models.EmailField(
        blank=True,
        null=True
    )

    validity = models.CharField(
        max_length=100,
        default="30 يوم"
    )

    # =========================================
    # SUBMITTED BY
    # =========================================

    submitted_by_name = models.CharField(
        max_length=255,
        default="روفانا تريد"
    )

    submitted_by_details = models.TextField(
        blank=True,
        null=True
    )

    # =========================================
    # SUBMITTED TO
    # =========================================

    submitted_to_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    submitted_to_details = models.TextField(
        blank=True,
        null=True
    )

    # =========================================
    # PROJECT
    # =========================================

    project_description = models.TextField(
        blank=True,
        null=True
    )

    # =========================================
    # FINANCIALS
    # =========================================

    vat_rate = models.FloatField(
        default=14
    )

    warning_note = models.TextField(
        default="الأسعار تقديرية وتخضع لأسعار المواد وقت التنفيذ وسعر الصرف."
    )

    # =========================================
    # DATES
    # =========================================
    
    payment_terms = models.TextField(
    default="""40% دفعة مقدمة عند تأكيد الطلب
    40% عند التسليم للموقع
    20% بعد إتمام التركيب والقبول"""
    )

    delivery_terms = models.TextField(
        default="""مدة التصنيع: تحدد عند الطلب
    التسليم: موقع العميل
    يشمل التغليف والشحن الداخلي"""
    )

    included_items = models.TextField(
        blank=True,
        null=True
    )

    excluded_items = models.TextField(
        blank=True,
        null=True

    )
    
    submitted_by_signature = models.CharField(
    max_length=255,
    default="روفانا تريد"
)

    client_signature = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    # =========================================
    # META
    # =========================================

    class Meta:

        ordering = ["-created_at"]

        verbose_name = "Quotation"

        verbose_name_plural = "Quotations"

    # =========================================
    # FUNCTIONS
    # =========================================

    def __str__(self):

        return self.quote_number

    @property
    def subtotal(self):

        total = 0

        for section in self.sections.all():

            for item in section.items.all():

                total += item.total_price

        return total

    @property
    def vat_amount(self):

        return (
            self.subtotal *
            self.vat_rate / 100
        )

    @property
    def grand_total(self):

        return (
            self.subtotal +
            self.vat_amount
        )


# =========================================
# QUOTE SECTION
# =========================================

class QuoteSection(models.Model):

    quotation = models.ForeignKey(
        Quotation,
        on_delete=models.CASCADE,
        related_name="sections"
    )

    title = models.CharField(
        max_length=255,
        default="قسم جديد"
    )

    sort_order = models.IntegerField(
        default=0
    )

    class Meta:

        ordering = ["sort_order"]

    def __str__(self):

        return (
            f"{self.quotation.quote_number}"
            f" - "
            f"{self.title}"
        )


# =========================================
# QUOTE ITEM
# =========================================

class QuoteItem(models.Model):

    section = models.ForeignKey(
        QuoteSection,
        on_delete=models.CASCADE,
        related_name="items"
    )

    description = models.TextField(
        blank=True,
        null=True
    )

    quantity = models.FloatField(
        default=1
    )

    unit = models.CharField(
        max_length=50,
        default="عدد"
    )

    unit_price = models.FloatField(
        default=0
    )

    total_price = models.FloatField(
        default=0
    )

    sort_order = models.IntegerField(
        default=0
    )

    class Meta:

        ordering = ["sort_order"]

    def save(self, *args, **kwargs):

        self.total_price = (
            float(self.quantity) *
            float(self.unit_price)
        )

        super().save(*args, **kwargs)

    def __str__(self):

        return (
            f"{self.section.title}"
            f" - "
            f"{self.description}"
        )