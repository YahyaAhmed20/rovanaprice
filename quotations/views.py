import json

from django.shortcuts import (
render,
get_object_or_404
)

from django.http import JsonResponse

from django.views.decorators.http import (
require_POST
)

from .models import (
Quotation,
QuoteSection,
QuoteItem,
Unit
)

from .utils import generate_quote_number

    # =========================

    # QUOTATION EDITOR PAGE

    # =========================

def quotation_editor(request, pk):
    
    quotation = get_object_or_404(
        Quotation,
        id=pk
    )

    return render(

        request,

        "quotations/add_price.html",

        {

            "quotation": quotation,

            "units": Unit.objects.filter(
                is_active=True
            )

    }

)


    # =========================

    # CREATE NEW QUOTATION

    # =========================

@require_POST
def create_quotation(request):

    
    quotation = Quotation.objects.create(
        quote_number=generate_quote_number()
    )

    return JsonResponse({

        "success": True,

        "id":
            quotation.id,

        "quote_number":
            quotation.quote_number

    })


    # =========================

    # UPDATE QUOTATION FIELDS

    # =========================

@require_POST
def update_quotation_field(request, pk):

    
    quotation = get_object_or_404(
        Quotation,
        id=pk
    )

    data = json.loads(
        request.body
    )

    field = data.get("field")

    value = data.get("value")


    allowed_fields = [

        "reference_number",

        "tag",

        "material",

        "customer_phone",

        "customer_email",

        "validity",

        "submitted_by_name",

        "submitted_by_details",

        "submitted_to_name",

        "submitted_to_details",

        "project_description",

        "vat_rate",

        "warning_note",
        "payment_terms",
        "delivery_terms",
        "included_items",
        "excluded_items",
        
        "submitted_by_signature",
        "client_signature"

    ]


    if field not in allowed_fields:

        return JsonResponse({
            "success": False,
            "message": "Invalid field"
        })


    # Handle float fields

    if field in [

        "vat_rate"

    ]:

        value = float(value or 0)


    setattr(
        quotation,
        field,
        value
    )

    quotation.save()


    return JsonResponse({

        "success": True

    })
    

    # =========================

    # CREATE SECTION

    # =========================

@require_POST
def create_section(request, pk):

    
    quotation = get_object_or_404(
        Quotation,
        id=pk
    )

    last_section = quotation.sections.order_by(
        "-sort_order"
    ).first()


    next_order = 1

    if last_section:

        next_order = (
            last_section.sort_order + 1
        )


    section = QuoteSection.objects.create(

        quotation=quotation,

        sort_order=next_order

    )


    return JsonResponse({

        "success": True,

        "section_id":
            section.id

    })
    

    # =========================

    # UPDATE SECTION

    # =========================

@require_POST
def update_section(request, section_id):

    
    section = get_object_or_404(
        QuoteSection,
        id=section_id
    )

    data = json.loads(
        request.body
    )

    title = data.get("title")


    section.title = title

    section.save()


    return JsonResponse({

        "success": True

    })
    

    # =========================

    # DELETE SECTION

    # =========================

@require_POST
def delete_section(request, section_id):

    
    section = get_object_or_404(
        QuoteSection,
        id=section_id
    )

    section.delete()


    return JsonResponse({

        "success": True

    })
    

    # =========================

    # CREATE ITEM

    # =========================

@require_POST
def create_item(request, section_id):

    section = get_object_or_404(
        QuoteSection,
        id=section_id
    )

    last_item = section.items.order_by(
        "-sort_order"
    ).first()

    next_order = 1

    if last_item:

        next_order = (
            last_item.sort_order + 1
        )

    item = QuoteItem.objects.create(
        section=section,
        sort_order=next_order
    )

    return JsonResponse({

        "success": True,

        "item_id": item.id

    })


    # =========================

    # UPDATE ITEM

    # =========================

@require_POST
def update_item(request, item_id):

    
    item = get_object_or_404(
        QuoteItem,
        id=item_id
    )


    data = json.loads(
        request.body
    )


    field = data.get("field")

    value = data.get("value")


    allowed_fields = [

        "description",

        "quantity",

        "unit",

        "unit_price",
       

    ]


    if field not in allowed_fields:

        return JsonResponse({

            "success": False,

            "message": "Invalid field"

        })


    if field in [

        "quantity",

        "unit_price"

    ]:

        value = float(value or 0)


    setattr(
        item,
        field,
        value
    )

    item.save()


    return JsonResponse({

        "success": True,

        "total_price":
            item.total_price

    })
    

    # =========================

    # DELETE ITEM

    # =========================

@require_POST
def delete_item(request, item_id):

    
    item = get_object_or_404(
        QuoteItem,
        id=item_id
    )

    item.delete()


    return JsonResponse({

        "success": True

    })


    # =========================

    # QUOTATIONS LIST PAGE

    # =========================

def quotations_list(request):
        

    quotations = Quotation.objects.all().order_by(
        "-created_at"
    )

    return render(

        request,

        "quotations/quotations_list.html",

        {

            "quotations": quotations

        }

    )



@require_POST
def delete_quotation(request, pk):

    quotation = get_object_or_404(
        Quotation,
        id=pk
    )

    quotation.delete()

    return JsonResponse({

        "success": True

    })