from django.urls import path

from . import views

app_name = "travel"

urlpatterns = [
    path("", views.home, name="home"),
    path("destinations/", views.destination_list, name="destination_list"),
    path("destinations/<slug:slug>/", views.destination_detail, name="destination_detail"),
    path("packages/", views.package_list, name="package_list"),
    path("packages/<int:pk>/book/", views.package_book, name="package_book"),
    path("search/", views.search, name="search"),
    path("about/", views.about, name="about"),
    path("contact/", views.contact, name="contact"),
    path("newsletter-subscribe/", views.newsletter_subscribe, name="newsletter_subscribe"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("trips/create/", views.trip_create, name="trip_create"),
    path("trips/", views.trip_list, name="my_trips"),
    path("trips/<int:trip_id>/", views.trip_detail, name="trip_detail"),
    path("trips/<int:trip_id>/edit/", views.trip_edit, name="trip_edit"),
    path("trips/<int:trip_id>/delete/", views.trip_delete, name="trip_delete"),
    path("trips/<int:trip_id>/itinerary/", views.itinerary_builder, name="itinerary_builder"),
    path(
        "trips/<int:trip_id>/city-stop/<int:stop_id>/<str:direction>/",
        views.city_stop_move,
        name="city_stop_move",
    ),
    path("trips/<int:trip_id>/timeline/", views.itinerary_timeline, name="itinerary_timeline"),
    path("city-search/", views.city_search, name="city_search"),
    path("activity-search/", views.activity_search, name="activity_search"),
    path("activity/<int:activity_id>/delete/", views.activity_delete, name="activity_delete"),
    path("trips/<int:trip_id>/budget/", views.budget_breakdown, name="budget_breakdown"),
    path("trips/<int:trip_id>/packing/", views.packing_checklist, name="packing_checklist"),
    path(
        "trips/<int:trip_id>/packing/<int:item_id>/toggle/",
        views.packing_toggle,
        name="packing_toggle",
    ),
    path(
        "trips/<int:trip_id>/packing/<int:item_id>/delete/",
        views.packing_delete,
        name="packing_delete",
    ),
    path("trips/<int:trip_id>/notes/", views.notes_page, name="notes_page"),
    path("trips/<int:trip_id>/notes/<int:note_id>/edit/", views.note_edit, name="note_edit"),
    path(
        "trips/<int:trip_id>/notes/<int:note_id>/delete/",
        views.note_delete,
        name="note_delete",
    ),
    path("profile/", views.profile_page, name="profile"),
    path("profile/delete/", views.delete_account, name="delete_account"),
    path("destinations/<slug:slug>/save/", views.toggle_save_destination, name="toggle_save_destination"),
    path("share/<uuid:slug>/", views.public_itinerary, name="public_itinerary"),
    path("admin-dashboard/", views.analytics_dashboard, name="analytics_dashboard"),
    path("activity/<int:activity_id>/update-date/", views.activity_update_date, name="activity_update_date"),
    path("activity/<int:activity_id>/quick-edit/", views.activity_quick_edit, name="activity_quick_edit"),
    path("debug/", views.debug_db),
]
