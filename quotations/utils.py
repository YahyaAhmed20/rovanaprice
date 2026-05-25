from django.utils.timezone import now

from .models import Quotation


def generate_quote_number():

    current_year = now().year

    last_quote = (

        Quotation.objects
        .filter(
            quote_number__startswith=
            f"QT-{current_year}"
        )
        .order_by("-id")
        .first()

    )

    if last_quote:

        try:

            last_number = int(

                last_quote.quote_number
                .split("-")[-1]

            )

        except:

            last_number = 0

    else:

        last_number = 0

    new_number = last_number + 1

    return (

        f"QT-{current_year}-"
        f"{new_number:03d}"

    )