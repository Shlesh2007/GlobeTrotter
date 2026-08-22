"""Main views for Traveloop travel planning flows."""
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import (
    ActivityForm,
    BudgetForm,
    CityStopForm,
    NoteForm,
    PackingItemForm,
    ProfileForm,
    SearchForm,
    TripForm,
    BookingForm,
)
from .models import Activity, Budget, CityStop, Note, PackingItem, Trip, UserProfile, Destination, Package


def _user_trip_or_404(user, trip_id):
    return get_object_or_404(Trip, pk=trip_id, user=user)


@login_required
def dashboard(request):
    sort_by = request.GET.get('sort', 'newest')
    filter_by = request.GET.get('filter', None)
    now = timezone.localdate()
    
    trips_query = Trip.objects.filter(user=request.user).prefetch_related("city_stops")
    
    if filter_by == 'upcoming':
        trips_query = trips_query.filter(start_date__gte=now)
    elif filter_by == 'past':
        trips_query = trips_query.filter(start_date__lt=now)
        
    if sort_by == 'oldest':
        trips = trips_query.order_by("start_date")[:5]
    else:
        trips = trips_query.order_by("-start_date")[:5]
        
    upcoming = Trip.objects.filter(user=request.user, start_date__gte=now).order_by("start_date")[:3]
    total_budget = sum([trip.total_budget for trip in Trip.objects.filter(user=request.user)])
    recent_activities = Activity.objects.filter(city_stop__trip__user=request.user).select_related("city_stop")[:5]

    recommended = Destination.objects.all().order_by('?')[:4]
    if not recommended.exists():
        # Fallback just in case
        recommended = []
        
    context = {
        "trips_count": Trip.objects.filter(user=request.user).count(),
        "city_count": CityStop.objects.filter(trip__user=request.user).count(),
        "activity_count": Activity.objects.filter(city_stop__trip__user=request.user).count(),
        "total_budget": total_budget,
        "upcoming_trips": upcoming,
        "recent_trips": trips,
        "recent_activities": recent_activities,
        "recommended_destinations": recommended,
    }
    return render(request, "travel/dashboard.html", context)


@login_required
def trip_create(request):
    if request.method == "POST":
        form = TripForm(request.POST, request.FILES)
        if form.is_valid():
            trip = form.save(commit=False)
            trip.user = request.user
            trip.save()
            
            suggested_cover_url = request.POST.get('suggested_cover_url')
            if suggested_cover_url and not trip.cover_image:
                import urllib.request
                import os
                from django.core.files import File
                
                try:
                    result = urllib.request.urlretrieve(suggested_cover_url)
                    trip.cover_image.save(
                        'suggested_cover.jpg',
                        File(open(result[0], 'rb'))
                    )
                except Exception:
                    pass
                    
            Budget.objects.get_or_create(trip=trip)
            messages.success(request, "Trip created successfully.")
            return redirect("travel:trip_detail", trip_id=trip.id)
    else:
        form = TripForm()
    return render(request, "travel/trip_form.html", {"form": form, "page_title": "Create Trip"})


@login_required
def trip_list(request):
    now = timezone.localdate()
    all_trips = Trip.objects.filter(user=request.user).order_by("start_date")
    
    ongoing_trips = []
    upcoming_trips = []
    completed_trips = []
    
    for trip in all_trips:
        if trip.end_date and trip.end_date < now:
            completed_trips.append(trip)
        elif trip.start_date and trip.start_date > now:
            upcoming_trips.append(trip)
        else:
            ongoing_trips.append(trip)
            
    # Sort completed trips by most recent first
    completed_trips.sort(key=lambda t: t.end_date if t.end_date else now, reverse=True)
            
    return render(request, "travel/my_trips.html", {
        "ongoing_trips": ongoing_trips,
        "upcoming_trips": upcoming_trips,
        "completed_trips": completed_trips,
    })


@login_required
def trip_detail(request, trip_id):
    trip = _user_trip_or_404(request.user, trip_id)
    city_stops = trip.city_stops.prefetch_related("activities").all()
    notes = trip.notes.all()[:5]
    return render(
        request,
        "travel/trip_detail.html",
        {"trip": trip, "city_stops": city_stops, "notes": notes},
    )


@login_required
def trip_edit(request, trip_id):
    trip = _user_trip_or_404(request.user, trip_id)
    if request.method == "POST":
        form = TripForm(request.POST, request.FILES, instance=trip)
        if form.is_valid():
            form.save()
            messages.success(request, "Trip updated.")
            return redirect("travel:trip_detail", trip_id=trip.id)
    else:
        form = TripForm(instance=trip)
    return render(request, "travel/trip_form.html", {"form": form, "page_title": "Edit Trip"})


@login_required
@require_POST
def trip_delete(request, trip_id):
    trip = _user_trip_or_404(request.user, trip_id)
    trip.delete()
    messages.success(request, "Trip deleted.")
    return redirect("travel:my_trips")


@login_required
def itinerary_builder(request, trip_id):
    trip = _user_trip_or_404(request.user, trip_id)
    city_form = CityStopForm(prefix="city")
    activity_form = ActivityForm(prefix="activity")
    activity_form.fields["city_stop"].queryset = trip.city_stops.all()

    if request.method == "POST":
        action = request.POST.get("action")
        if action == "add_city":
            city_form = CityStopForm(request.POST, prefix="city")
            if city_form.is_valid():
                city = city_form.save(commit=False)
                city.trip = trip
                city.save()
                messages.success(request, "City stop added.")
                return redirect("travel:itinerary_builder", trip_id=trip.id)
        elif action == "add_activity":
            activity_form = ActivityForm(request.POST, prefix="activity")
            activity_form.fields["city_stop"].queryset = trip.city_stops.all()
            if activity_form.is_valid():
                activity = activity_form.cleaned_data["city_stop"]
                if activity.trip_id != trip.id:
                    raise Http404("Invalid city stop.")
                activity_form.save()
                messages.success(request, "Activity added.")
                return redirect("travel:itinerary_builder", trip_id=trip.id)

    city_stops = trip.city_stops.prefetch_related("activities")
    return render(
        request,
        "travel/itinerary_builder.html",
        {"trip": trip, "city_form": city_form, "activity_form": activity_form, "city_stops": city_stops},
    )


@login_required
def city_stop_move(request, trip_id, stop_id, direction):
    trip = _user_trip_or_404(request.user, trip_id)
    stop = get_object_or_404(CityStop, pk=stop_id, trip=trip)
    if direction == "up":
        target = CityStop.objects.filter(trip=trip, order__lt=stop.order).order_by("-order").first()
    else:
        target = CityStop.objects.filter(trip=trip, order__gt=stop.order).order_by("order").first()
    if target:
        original_stop_order = stop.order
        original_target_order = target.order
        
        # Temporarily assign a high order to avoid unique constraint violation
        stop.order = 99999
        stop.save(update_fields=['order'])
        
        target.order = original_stop_order
        target.save(update_fields=['order'])
        
        stop.order = original_target_order
        stop.save(update_fields=['order'])
    return redirect("travel:itinerary_builder", trip_id=trip.id)


@login_required
def itinerary_timeline(request, trip_id):
    trip = _user_trip_or_404(request.user, trip_id)
    city_stops = trip.city_stops.prefetch_related("activities").all()
    activities = Activity.objects.filter(city_stop__trip=trip).order_by("activity_date")

    day_map = {}
    total_activities_cost = 0
    for activity in activities:
        day_map.setdefault(activity.activity_date, []).append(activity)
        if activity.cost:
            total_activities_cost += activity.cost

    return render(
        request,
        "travel/itinerary_timeline.html",
        {
            "trip": trip, 
            "city_stops": city_stops, 
            "day_map": day_map,
            "total_activities_cost": total_activities_cost,
        },
    )


@login_required
def city_search(request):
    form = SearchForm(request.GET or None)
    destinations = Destination.objects.all()
    
    country_filter = request.GET.get('country')
    if country_filter:
        destinations = destinations.filter(country__iexact=country_filter)
        
    if form.is_valid():
        q = (form.cleaned_data.get("q") or "").strip()
        if q:
            destinations = destinations.filter(Q(name__icontains=q) | Q(country__icontains=q))
            
    countries = Destination.objects.values_list('country', flat=True).distinct()
    user_trips = Trip.objects.filter(user=request.user)

    if request.method == "POST":
        trip_id = request.POST.get("trip_id")
        dest_id = request.POST.get("dest_id")
        if trip_id and dest_id:
            trip = get_object_or_404(Trip, id=trip_id, user=request.user)
            dest = get_object_or_404(Destination, id=dest_id)
            
            from django.db.models import Max
            max_order = CityStop.objects.filter(trip=trip).aggregate(Max('order'))['order__max'] or 0
            
            CityStop.objects.create(
                trip=trip,
                city_name=dest.name,
                country=dest.country,
                arrival_date=trip.start_date,
                departure_date=trip.start_date,
                order=max_order + 1
            )
            messages.success(request, f"{dest.name} added to {trip.title}!")
            return redirect("travel:itinerary_builder", trip_id=trip.id)

    return render(request, "travel/city_search.html", {
        "form": form, 
        "destinations": destinations, 
        "countries": countries,
        "user_trips": user_trips,
        "selected_country": country_filter
    })


@login_required
@require_POST
def activity_delete(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id, city_stop__trip__user=request.user)
    trip_id = activity.city_stop.trip.id
    activity.delete()
    messages.info(request, "Activity removed.")
    # Redirect back to referring page, so it works from both Builder and Search
    return redirect(request.META.get('HTTP_REFERER', 'travel:itinerary_builder'))

CATALOG_ACTIVITIES = [
    {
        "id": 1,
        "title": "Guided City Tour",
        "category": "sightseeing",
        "description": "Explore the city's main landmarks with an expert guide.",
        "cost": 2500,
        "duration_hours": 3.0,
        "image_url": "https://loremflickr.com/600/400/tour?lock=501",
    },
    {
        "id": 2,
        "title": "Local Food Tasting",
        "category": "food",
        "description": "Sample authentic local dishes at top-rated street stalls.",
        "cost": 1500,
        "duration_hours": 2.5,
        "image_url": "https://loremflickr.com/600/400/food?lock=502",
    },
    {
        "id": 3,
        "title": "Mountain Hiking",
        "category": "adventure",
        "description": "A thrilling day hike with breathtaking panoramic views.",
        "cost": 0,
        "duration_hours": 5.0,
        "image_url": "https://loremflickr.com/600/400/mountain?lock=503",
    },
    {
        "id": 4,
        "title": "Museum Pass",
        "category": "culture",
        "description": "Skip-the-line access to the top 3 museums in the area.",
        "cost": 3000,
        "duration_hours": 4.0,
        "image_url": "https://loremflickr.com/600/400/museum?lock=504",
    },
    {
        "id": 5,
        "title": "Traditional Market Shopping",
        "category": "shopping",
        "description": "Browse artisan crafts and souvenirs in the historic market.",
        "cost": 500,
        "duration_hours": 2.0,
        "image_url": "https://loremflickr.com/600/400/shopping?lock=505",
    }
]

@login_required
def activity_search(request):
    form = SearchForm(request.GET or None)
    activities = CATALOG_ACTIVITIES
    
    cat_filter = request.GET.get('category')
    if cat_filter:
        activities = [a for a in activities if a["category"] == cat_filter]
        
    if form.is_valid():
        q = (form.cleaned_data.get("q") or "").strip().lower()
        if q:
            activities = [a for a in activities if q in a["title"].lower() or q in a["description"].lower()]

    categories = Activity.CATEGORY_CHOICES
    user_city_stops = CityStop.objects.filter(trip__user=request.user).select_related('trip')

    if request.method == "POST":
        stop_id = request.POST.get("stop_id")
        act_id = request.POST.get("activity_id")
        
        if stop_id and act_id:
            stop = get_object_or_404(CityStop, id=stop_id, trip__user=request.user)
            catalog_item = next((a for a in CATALOG_ACTIVITIES if str(a["id"]) == str(act_id)), None)
            
            if catalog_item:
                Activity.objects.create(
                    city_stop=stop,
                    title=catalog_item["title"],
                    category=catalog_item["category"],
                    description=catalog_item["description"],
                    cost=catalog_item["cost"],
                    duration_hours=catalog_item["duration_hours"],
                    activity_date=stop.arrival_date
                )
                messages.success(request, f"{catalog_item['title']} added to {stop.city_name}!")
                return redirect("travel:itinerary_builder", trip_id=stop.trip.id)

    user_activities = Activity.objects.filter(city_stop__trip__user=request.user).select_related('city_stop__trip')

    return render(request, "travel/activity_search.html", {
        "form": form, 
        "activities": activities,
        "categories": categories,
        "selected_category": cat_filter,
        "user_city_stops": user_city_stops,
        "user_activities": user_activities
    })


@login_required
def budget_breakdown(request, trip_id):
    trip = _user_trip_or_404(request.user, trip_id)
    budget, _ = Budget.objects.get_or_create(trip=trip)
    if request.method == "POST":
        form = BudgetForm(request.POST, instance=budget)
        if form.is_valid():
            form.save()
            messages.success(request, "Budget updated.")
            return redirect("travel:budget_breakdown", trip_id=trip.id)
    else:
        form = BudgetForm(instance=budget)

    total = budget.total_cost
    avg_daily = total / trip.total_days if trip.total_days else 0
    chart_data = {
        "labels": ["Transport", "Hotel", "Food", "Activities", "Misc"],
        "values": [
            float(budget.transport_cost),
            float(budget.hotel_cost),
            float(budget.food_cost),
            float(budget.activity_cost),
            float(budget.miscellaneous_cost),
        ],
    }

    from decimal import Decimal

    # Calculate actual expenses per day from itinerary activities
    activities = Activity.objects.filter(city_stop__trip=trip)
    day_costs = {}
    total_actual_expenses = Decimal('0.00')
    
    for activity in activities:
        if activity.cost:
            day_costs[activity.activity_date] = day_costs.get(activity.activity_date, Decimal('0.00')) + activity.cost
            total_actual_expenses += activity.cost

    remaining_budget = Decimal(total) - total_actual_expenses

    overbudget_days = []
    
    # Calculate exact daily budget
    avg_daily_decimal = Decimal(total) / Decimal(trip.total_days) if trip.total_days else Decimal('0.00')

    if avg_daily_decimal > 0:
        for day, cost in day_costs.items():
            if cost > avg_daily_decimal:
                over_amount = cost - avg_daily_decimal
                overbudget_days.append({
                    "date": day,
                    "cost": cost,
                    "over_amount": over_amount
                })
    # Sort overbudget days chronologically
    overbudget_days.sort(key=lambda x: x["date"])

    return render(
        request,
        "travel/budget_breakdown.html",
        {
            "trip": trip,
            "form": form,
            "budget": budget,
            "total": total,
            "avg_daily": avg_daily_decimal,
            "total_actual_expenses": total_actual_expenses,
            "remaining_budget": remaining_budget,
            "chart_data": chart_data,
            "overbudget_days": overbudget_days,
        },
    )


@login_required
def packing_checklist(request, trip_id):
    trip = _user_trip_or_404(request.user, trip_id)
    form = PackingItemForm()
    if request.method == "POST":
        form = PackingItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            item.trip = trip
            item.save()
            messages.success(request, "Packing item added.")
            return redirect("travel:packing_checklist", trip_id=trip.id)
    category = request.GET.get("category", "")
    items = trip.packing_items.all()
    if category:
        items = items.filter(category=category)
    return render(request, "travel/packing_checklist.html", {"trip": trip, "form": form, "items": items, "category": category})


@login_required
@require_POST
def packing_toggle(request, trip_id, item_id):
    trip = _user_trip_or_404(request.user, trip_id)
    item = get_object_or_404(PackingItem, pk=item_id, trip=trip)
    item.is_packed = not item.is_packed
    item.save()
    return redirect("travel:packing_checklist", trip_id=trip.id)


@login_required
@require_POST
def packing_delete(request, trip_id, item_id):
    trip = _user_trip_or_404(request.user, trip_id)
    item = get_object_or_404(PackingItem, pk=item_id, trip=trip)
    item.delete()
    messages.info(request, "Packing item removed.")
    return redirect("travel:packing_checklist", trip_id=trip.id)


@login_required
def notes_page(request, trip_id):
    trip = _user_trip_or_404(request.user, trip_id)
    form = NoteForm()
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.trip = trip
            note.save()
            messages.success(request, "Note saved.")
            return redirect("travel:notes_page", trip_id=trip.id)
    notes = trip.notes.all()
    return render(request, "travel/notes.html", {"trip": trip, "notes": notes, "form": form})


@login_required
def note_edit(request, trip_id, note_id):
    trip = _user_trip_or_404(request.user, trip_id)
    note = get_object_or_404(Note, pk=note_id, trip=trip)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, "Note updated.")
            return redirect("travel:notes_page", trip_id=trip.id)
    else:
        form = NoteForm(instance=note)
    return render(request, "travel/note_edit.html", {"trip": trip, "note": note, "form": form})


@login_required
@require_POST
def note_delete(request, trip_id, note_id):
    trip = _user_trip_or_404(request.user, trip_id)
    note = get_object_or_404(Note, pk=note_id, trip=trip)
    note.delete()
    messages.info(request, "Note deleted.")
    return redirect("travel:notes_page", trip_id=trip.id)


@login_required
def profile_page(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated.")
            return redirect("travel:profile")
    else:
        form = ProfileForm(instance=profile, user=request.user)
        
    saved_destinations = profile.saved_destinations.all()
    return render(request, "travel/profile.html", {"form": form, "profile": profile, "saved_destinations": saved_destinations})


@login_required
@require_POST
def delete_account(request):
    user = request.user
    user.delete()
    messages.success(request, "Your account has been permanently deleted.")
    return redirect("travel:home")


@login_required
@require_POST
def toggle_save_destination(request, slug):
    destination = get_object_or_404(Destination, slug=slug)
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    
    if destination in profile.saved_destinations.all():
        profile.saved_destinations.remove(destination)
        messages.info(request, f"{destination.name} removed from saved destinations.")
    else:
        profile.saved_destinations.add(destination)
        messages.success(request, f"{destination.name} added to saved destinations.")
        
    return redirect(request.META.get('HTTP_REFERER', 'travel:profile'))




def public_itinerary(request, slug):
    trip = get_object_or_404(Trip, public_slug=slug, is_public=True)
    city_stops = trip.city_stops.prefetch_related("activities").all()
    return render(request, "travel/public_itinerary.html", {"trip": trip, "city_stops": city_stops})

# Add these functions to travel/views.py

def home(request):
    from travel.models import Destination, Package, Testimonial
    from django.utils.text import slugify
    
    featured_destinations = Destination.objects.filter(featured=True)[:3]
    
    # Comprehensive Data Fix & Seed
    try:
        # Seed 8 new destinations if they don't exist
        new_dests = [
            ("Paris", "France", "City of Light and romance.", "Experience the Eiffel Tower, Louvre, and world-class cuisine.", True),
            ("Rome", "Italy", "The Eternal City.", "Ancient ruins, incredible pasta, and vibrant street life.", True),
            ("Bali", "Indonesia", "Tropical paradise.", "Lush jungles, ancient temples, and perfect surf breaks.", True),
            ("Tokyo", "Japan", "Neon lights and ancient traditions.", "A bustling metropolis blending the future with the past.", True),
            ("Dubai", "UAE", "Futuristic desert oasis.", "Luxury shopping, ultra-modern architecture, and lively nightlife.", True),
            ("Sydney", "Australia", "Harbor city down under.", "Iconic Opera House, Bondi Beach, and vibrant culture.", False),
            ("Amsterdam", "Netherlands", "Canals and bicycles.", "Historic waterways, world-class museums, and cozy cafes.", False),
            ("Machu Picchu", "Peru", "Ancient Incan citadel.", "Breathtaking mountain views and historical ruins.", True),
        ]
        
        for name, country, short_desc, desc, feat in new_dests:
            d, created = Destination.objects.get_or_create(
                name=name,
                defaults={
                    "country": country,
                    "short_description": short_desc,
                    "description": desc,
                    "featured": feat,
                    "slug": slugify(name),
                    "image_url": "temp"
                }
            )
            
        # Seed packages
        if Package.objects.count() < 10:
            for dest in Destination.objects.all()[:8]:
                Package.objects.get_or_create(
                    name=f"Ultimate {dest.name} Escape",
                    destination=dest,
                    defaults={
                        "headline": f"Discover the best of {dest.name} in 7 days.",
                        "description": f"An all-inclusive tour of {dest.name}. You will love everything about it.",
                        "duration_days": 7,
                        "price_per_person": 1299.00,
                        "max_travelers": 12,
                        "featured": True,
                        "image_url": "temp",
                        "slug": slugify(f"ultimate {dest.name} escape")
                    }
                )
                Package.objects.get_or_create(
                    name=f"{dest.name} Quick Getaway",
                    destination=dest,
                    defaults={
                        "headline": f"A fast-paced 3-day tour of {dest.name}.",
                        "description": "Perfect for a weekend getaway.",
                        "duration_days": 3,
                        "price_per_person": 499.00,
                        "max_travelers": 8,
                        "featured": False,
                        "image_url": "temp",
                        "slug": slugify(f"{dest.name} quick getaway")
                    }
                )

        # Fix all images using keyword-based LoremFlickr to avoid Unsplash hotlinking blocks
        for d in Destination.objects.all():
            if not d.slug:
                d.slug = slugify(d.name)
            
            # Use LoremFlickr which supports keyword searches for relevant images!
            keyword = d.name.replace(" ", "")
            d.image_url = f"https://loremflickr.com/1400/800/{keyword}?lock={d.id + 3000}"
            d.save()
            
        for p in Package.objects.all():
            if not p.slug:
                p.slug = slugify(p.name)
            
            keyword = "travel"
            if p.destination:
                keyword = p.destination.name.replace(" ", "")
                
            p.image_url = f"https://loremflickr.com/1400/800/{keyword}?lock={p.id + 1000}"
            p.save()
            
        # Seed testimonials if empty
        if not Testimonial.objects.exists():
            Testimonial.objects.create(name="Sarah Jenkins", role="Solo Backpacker", quote="GlobeTrotter completely changed how I plan my trips. The seamless itinerary builder and the beautiful destination guides saved me hours of stress!", rating=5, featured=True)
            Testimonial.objects.create(name="David & Emma", role="Honeymooners", quote="Booking our trip to Santorini was an absolute breeze. The curated packages are perfectly tailored. Best travel experience we've ever had.", rating=5, featured=True)
            Testimonial.objects.create(name="Marcus Chen", role="Digital Nomad", quote="I rely on this platform for all my extended stays. The budget breakdown feature is a lifesaver for long-term travelers.", rating=4, featured=True)
            
    except Exception as e:
        messages.error(request, f"Data seed failed: {str(e)}")
            
    popular_packages = Package.objects.filter(featured=True)[:3]
    search_form = SearchForm()
    
    testimonials = Testimonial.objects.filter(featured=True)
    
    # Mock stats for the hero section
    stats = {
        "destinations": Destination.objects.count() or 12,
        "packages": Package.objects.count() or 45,
        "travelers_booked": 1200,
        "avg_rating": 4.9
    }
    
    return render(request, "travel/home.html", {
        "featured_destinations": featured_destinations,
        "popular_packages": popular_packages,
        "testimonials": testimonials,
        "search_form": search_form,
        "stats": stats
    })

def destination_list(request):
    destinations = Destination.objects.all()
    return render(request, "travel/destination_list.html", {"destinations": destinations})

def package_list(request):
    packages = Package.objects.all()
    return render(request, "travel/package_list.html", {"packages": packages})

def search(request):
    form = SearchForm(request.GET or None)
    destinations = Destination.objects.all()
    packages = Package.objects.all()
    
    if form.is_valid():
        q = (form.cleaned_data.get("q") or "").strip()
        if q:
            destinations = destinations.filter(Q(name__icontains=q) | Q(country__icontains=q))
            packages = packages.filter(Q(name__icontains=q) | Q(destination__name__icontains=q))
            
    return render(request, "travel/search.html", {
        "form": form,
        "destinations": destinations,
        "packages": packages
    })

@login_required
def package_book(request, pk):
    package = get_object_or_404(Package, pk=pk)
    
    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.package = package
            booking.total_price = booking.travelers_count * package.price_per_person
            booking.save()
            
            # Automatically create a Trip so the user can manage it in their dashboard
            from datetime import timedelta
            import requests
            from django.core.files.base import ContentFile
            
            end_date = booking.travel_date + timedelta(days=max(0, package.duration_days - 1))
            trip = Trip.objects.create(
                user=request.user,
                title=f"Package: {package.name}",
                description=f"Booked package for {booking.travelers_count} traveler(s).\n\n{package.description}",
                start_date=booking.travel_date,
                end_date=end_date,
            )
            
            # Fetch the package image and save it as the trip cover image
            if package.image_url:
                try:
                    img_response = requests.get(package.image_url, timeout=5)
                    if img_response.status_code == 200:
                        file_name = f"pkg_{package.id}_trip_{trip.id}.jpg"
                        trip.cover_image.save(file_name, ContentFile(img_response.content), save=True)
                except Exception:
                    pass
                    
            CityStop.objects.create(
                trip=trip,
                city_name=package.destination.name,
                country=package.destination.country,
                arrival_date=booking.travel_date,
                departure_date=end_date,
                order=1
            )
            
            messages.success(request, f"Successfully booked {package.name}!")
            return redirect("travel:dashboard")
    else:
        form = BookingForm(initial={'travelers_count': 1})
        
    return render(request, "travel/book_package.html", {
        "package": package, 
        "form": form,
        "price_per_person": package.price_per_person
    })

def newsletter_subscribe(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            from .models import NewsletterSubscriber
            NewsletterSubscriber.objects.get_or_create(email=email)
    return redirect(request.META.get("HTTP_REFERER", "travel:home"))
def about(request):
    return render(request, "travel/about.html")

def contact(request):
    return render(request, "travel/contact.html")

def destination_detail(request, slug):
    destination = get_object_or_404(Destination, slug=slug)
    packages = destination.packages.all()
    return render(request, "travel/destination_detail.html", {
        "destination": destination,
        "packages": packages
    })

@login_required
@require_POST
def activity_update_date(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id, city_stop__trip__user=request.user)
    new_date = request.POST.get("new_date")
    if new_date:
        activity.activity_date = new_date
        activity.save()
        import json
        from django.http import JsonResponse
        return JsonResponse({"status": "success"})
    return JsonResponse({"status": "error"}, status=400)

@login_required
@require_POST
def activity_quick_edit(request, activity_id):
    activity = get_object_or_404(Activity, pk=activity_id, city_stop__trip__user=request.user)
    
    title = request.POST.get("title")
    if title:
        activity.title = title
        
    cost = request.POST.get("cost")
    if cost:
        activity.cost = cost
        
    duration = request.POST.get("duration_hours")
    if duration:
        activity.duration_hours = duration
        
    desc = request.POST.get("description")
    if desc is not None:
        activity.description = desc
        
    act_date = request.POST.get("activity_date")
    if act_date:
        activity.activity_date = act_date
        
    activity.save()
    messages.success(request, "Activity updated.")
    return redirect(request.META.get("HTTP_REFERER", "travel:itinerary_timeline"))


from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count
from django.contrib.auth.models import User
from .models import Booking
import json

@user_passes_test(lambda u: u.is_staff)
def analytics_dashboard(request):
    total_users = User.objects.count()
    total_trips = Trip.objects.count()
    total_bookings = Booking.objects.count()

    top_cities_qs = CityStop.objects.values('city_name').annotate(count=Count('id')).order_by('-count')[:5]
    top_cities_labels = [item['city_name'] for item in top_cities_qs]
    top_cities_data = [item['count'] for item in top_cities_qs]

    top_activities_qs = Activity.objects.values('category').annotate(count=Count('id')).order_by('-count')[:5]
    top_activities_labels = [item['category'].capitalize() for item in top_activities_qs]
    top_activities_data = [item['count'] for item in top_activities_qs]

    context = {
        'total_users': total_users,
        'total_trips': total_trips,
        'total_bookings': total_bookings,
        'top_cities_labels_json': json.dumps(top_cities_labels),
        'top_cities_data_json': json.dumps(top_cities_data),
        'top_activities_labels_json': json.dumps(top_activities_labels),
        'top_activities_data_json': json.dumps(top_activities_data),
    }

    return render(request, "travel/analytics_dashboard.html", context)

def debug_db(request):
    import json
    from django.http import HttpResponse
    data = []
    for d in Destination.objects.all():
        data.append({'name': d.name, 'url': d.image_url})
    
    with open(r'd:\GlobeTrotter(LDEC_odoo)\db_dump.json', 'w') as f:
        json.dump(data, f, indent=2)
        
    return HttpResponse("Dumped to db_dump.json")