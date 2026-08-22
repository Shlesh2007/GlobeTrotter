"""Admin registrations for Traveloop planner."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import (
    Activity,
    Budget,
    CityStop,
    Note,
    PackingItem,
    Trip,
    UserProfile,
)


class UserProfileInline(admin.StackedInline):
    model = UserProfile
    fk_name = "user"
    can_delete = False
    verbose_name_plural = "Profile"


class UserAdmin(BaseUserAdmin):
    inlines = (UserProfileInline,)


admin.site.unregister(User)
admin.site.register(User, UserAdmin)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "phone", "preferred_travel_style")
    search_fields = ("user__username", "phone", "preferred_travel_style")


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "start_date", "end_date", "is_public", "created_at")
    list_filter = ("is_public", "start_date")
    search_fields = ("title", "user__username")


@admin.register(CityStop)
class CityStopAdmin(admin.ModelAdmin):
    list_display = ("city_name", "country", "trip", "arrival_date", "departure_date", "order")
    list_filter = ("country",)
    search_fields = ("city_name", "trip__title")


@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ("title", "city_stop", "category", "cost", "activity_date")
    list_filter = ("category", "activity_date")
    search_fields = ("title", "city_stop__city_name")


@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ("trip", "transport_cost", "hotel_cost", "food_cost", "activity_cost", "miscellaneous_cost")


@admin.register(PackingItem)
class PackingItemAdmin(admin.ModelAdmin):
    list_display = ("item_name", "trip", "category", "is_packed")
    list_filter = ("category", "is_packed")
    search_fields = ("item_name", "trip__title")


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ("title", "trip", "created_at")
    search_fields = ("title", "trip__title")
    ordering = ("-created_at",)


# Friendly admin branding
admin.site.site_header = "GlobeTrotter Admin"
admin.site.site_title = "GlobeTrotter"
admin.site.index_title = "Manage planners, itinerary data, and users"
