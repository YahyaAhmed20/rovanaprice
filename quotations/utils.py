from .models import Quotation


def generate_quote_number():

    last_quote = Quotation.objects.count() + 1

    return f"QT-2026-{last_quote:03d}"