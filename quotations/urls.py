from django.urls import path

from . import views

app_name = "quotations"

urlpatterns = [

    # =========================
    # HOME
    # =========================

    path(
        "",
        views.quotations_list,
        name="home"
    ),

    # =========================
    # QUOTATION PAGES
    # =========================

    path(
        "quotation/<int:pk>/",
        views.quotation_editor,
        name="quotation_editor"
    ),

    path(
        "quotations/",
        views.quotations_list,
        name="quotations_list"
    ),

    # =========================
    # QUOTATION APIs
    # =========================

    path(
        "api/quotation/create/",
        views.create_quotation,
        name="create_quotation"
    ),

    path(
        "api/quotation/<int:pk>/update/",
        views.update_quotation_field,
        name="update_quotation_field"
    ),

    path(
        "api/quotation/<int:pk>/delete/",
        views.delete_quotation,
        name="delete_quotation"
    ),

    # =========================
    # SECTION APIs
    # =========================

    path(
        "api/quotation/<int:pk>/section/create/",
        views.create_section,
        name="create_section"
    ),

    path(
        "api/section/<int:section_id>/update/",
        views.update_section,
        name="update_section"
    ),

    path(
        "api/section/<int:section_id>/delete/",
        views.delete_section,
        name="delete_section"
    ),

    # =========================
    # ITEM APIs
    # =========================

    path(
        "api/section/<int:section_id>/item/create/",
        views.create_item,
        name="create_item"
    ),

    path(
        "api/item/<int:item_id>/update/",
        views.update_item,
        name="update_item"
    ),

    path(
        "api/item/<int:item_id>/delete/",
        views.delete_item,
        name="delete_item"
    ),

]