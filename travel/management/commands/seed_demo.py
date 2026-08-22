"""
Populate the database with attractive demo content (safe to run multiple times).
Usage: python manage.py seed_demo
"""
from decimal import Decimal

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.utils.text import slugify

from travel.models import (
    Booking,
    Destination,
    Package,
    UserProfile,
    Trip,
    Testimonial,          # Add this line
    NewsletterSubscriber, # Add this line
)
# Note: Remove Testimonial and NewsletterSubscriber from the import 
# if you haven't added those models back yet.


class Command(BaseCommand):
    help = "Create sample destinations, packages, testimonials, and a demo login."

    def handle(self, *args, **options):
        # --- Demo user ---
        demo_user, _ = User.objects.get_or_create(
            username="traveler_demo",
            defaults={
                "email": "demo@traveloop.com",
                "first_name": "Alex",
                "last_name": "Explorer",
            },
        )
        if not demo_user.has_usable_password():
            demo_user.set_password("demo12345")
            demo_user.save()
        UserProfile.objects.get_or_create(
            user=demo_user,
            defaults={"phone": "+1 555 010 2030", "country": "United States"},
        )
        self.stdout.write(self.style.SUCCESS("Demo login: traveler_demo / demo12345"))

        # --- Destinations (Unsplash image URLs) ---
        dest_data = [
            {
                "name": "Santorini",
                "country": "Greece",
                "short_description": "White villages, cobalt seas, sunsets over the Caldera.",
                "description": (
                    "Wander cliffside paths in Oia, taste island wines, and sail the Aegean on a boutique catamaran. "
                    "Perfect for honeymooners and slow travelers."
                ),
                "image_url": (
                    "https://images.unsplash.com/photo-1613395877344-13c474d42728?auto=format&fit=crop&w=1400&q=80"
                ),
                "featured": True,
                "slug": "santorini-greece",
            },
            {
                "name": "Kyoto",
                "country": "Japan",
                "short_description": "Ancient temples meet bamboo forests and tea houses.",
                "description": (
                    "Experience zen gardens at dawn, Michelin-level kaiseki, and the philosopher's path in cherry blossom season."
                ),
                "image_url": (
                    "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e?auto=format&fit=crop&w=1400&q=80"
                ),
                "featured": True,
                "slug": "kyoto-japan",
            },
            {
                "name": "Swiss Alps",
                "country": "Switzerland",
                "short_description": "Mountain peaks, scenic trains, and lakeside serenity.",
                "description": (
                    "From Zermatt's Matterhorn views to emerald lakes near Interlaken — hiking, spas, and chocolate included."
                ),
                "image_url": (
                    "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?auto=format&fit=crop&w=1400&q=80"
                ),
                "featured": True,
                "slug": "swiss-alps-switzerland",
            },
            {
                "name": "Banff National Park",
                "country": "Canada",
                "short_description": "Turquoise lakes, wildlife, and endless alpine trails.",
                "description": (
                    "Canoe Lake Louise, soak in Banff Upper Hot Springs, and chase aurora-lit skies in winter."
                ),
                "image_url": (
                    "https://images.unsplash.com/photo-1517935706615-2717063c2225?auto=format&fit=crop&w=1400&q=80"
                ),
                "featured": False,
                "slug": "banff-canada",
            },
        ]

        destinations = {}
        for d in dest_data:
            slug = d.pop("slug")
            obj, _ = Destination.objects.update_or_create(
                slug=slug,
                defaults={**d, "slug": slug},
            )
            destinations[slug] = obj

        # --- Packages ---
        pkgs = [
            {
                "dest": "santorini-greece",
                "name": "Aegean Sunsets Deluxe",
                "headline": "5 nights cliffside bliss + sunset cruise.",
                "description": (
                    "Boutique hotel, daily breakfast, private wine tasting, and a half-day yacht experience."
                ),
                "duration_days": 5,
                "price": Decimal("1899.00"),
                "max_travelers": 6,
                "image_url": (
                    "https://images.unsplash.com/photo-1533105079780-92b9be482077?auto=format&fit=crop&w=1200&q=80"
                ),
                "featured": True,
            },
            {
                "dest": "santorini-greece",
                "name": "Island Hopping Essentials",
                "headline": "Flexible island entry — ideal for explorers.",
                "description": (
                    "Ferry hops, scooter rental vouchers, curated walking maps, and 24/7 concierge chat."
                ),
                "duration_days": 4,
                "price": Decimal("1049.00"),
                "max_travelers": 8,
                "image_url": (
                    "https://images.unsplash.com/photo-1602002418082-a4443e081dd1?auto=format&fit=crop&w=1200&q=80"
                ),
                "featured": True,
            },
            {
                "dest": "kyoto-japan",
                "name": "Temple Trails & Tea",
                "headline": "Immersive Kyoto culture curated by locals.",
                "description": "Tea ceremony workshop, kimono stroll in Gion, and early access temple visits.",
                "duration_days": 6,
                "price": Decimal("2249.50"),
                "max_travelers": 5,
                "image_url": (
                    "https://images.unsplash.com/photo-1528360983277-13d401cdc186?auto=format&fit=crop&w=1200&q=80"
                ),
                "featured": True,
            },
            {
                "dest": "swiss-alps-switzerland",
                "name": "Glacier Express Journey",
                "headline": "Panoramic trains + alpine spa breaks.",
                "description": (
                    "First-class rail passes, luxury chalet stays, fondue tastings, and optional paragliding."
                ),
                "duration_days": 7,
                "price": Decimal("3299.00"),
                "max_travelers": 4,
                "image_url": (
                    "https://images.unsplash.com/photo-1502780402662-acc019171eec?auto=format&fit=crop&w=1200&q=80"
                ),
                "featured": True,
            },
            {
                "dest": "banff-canada",
                "name": "Rockies Classic Road Trip",
                "headline": "Lake Louise & Icefields Parkway essentials.",
                "description": (
                    "SUV hire, curated hiking routes, and a guided wildlife dusk safari."
                ),
                "duration_days": 5,
                "price": Decimal("1649.00"),
                "max_travelers": 6,
                "image_url": (
                    "https://images.unsplash.com/photo-1464822759844-d150ee613b5c?auto=format&fit=crop&w=1200&q=80"
                ),
                "featured": False,
            },
        ]

        packages = []
        for p in pkgs:
            dest = destinations[p["dest"]]
            pname = p["name"]
            pslug = slugify(f"{pname}-{dest.slug}")
            pkg, created = Package.objects.update_or_create(
                destination=dest,
                slug=pslug,
                defaults={
                    "name": pname,
                    "headline": p["headline"],
                    "description": p["description"],
                    "duration_days": p["duration_days"],
                    "price_per_person": p["price"],
                    "max_travelers": p["max_travelers"],
                    "image_url": p["image_url"],
                    "featured": p["featured"],
                },
            )
            packages.append(pkg)
            flag = "created" if created else "updated"
            self.stdout.write(f"Package {flag}: {pkg.name}")

        # --- Demo booking ---
        if packages:
            Booking.objects.get_or_create(
                user=demo_user,
                package=packages[0],
                travel_date="2027-06-01",
                defaults={
                    "travelers_count": 2,
                    "total_price": packages[0].price_per_person * 2,
                    "status": Booking.STATUS_CONFIRMED,
                },
            )

        # --- Testimonials ---
        quotes = [
            {
                "name": "Sophie Laurent",
                "role": "Product designer · Paris",
                "quote": "Traveloop nailed every transfer and hotel upgrade. Santorini felt effortless.",
                "rating": 5,
                "avatar": "https://images.unsplash.com/photo-1438761681033-6461ffad8d80?auto=format&fit=crop&w=200&q=80",
            },
            {
                "name": "Jordan Kim",
                "role": "Founder · Seattle",
                "quote": "The Kyoto itinerary balanced iconic sights with quiet neighborhood gems.",
                "rating": 5,
                "avatar": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?auto=format&fit=crop&w=200&q=80",
            },
            {
                "name": "Maya Torres",
                "role": "Photographer · Mexico City",
                "quote": "Swiss rail journey was cinematic. Support answered in minutes on WhatsApp.",
                "rating": 5,
                "avatar": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?auto=format&fit=crop&w=200&q=80",
            },
        ]
        for t in quotes:
            Testimonial.objects.get_or_create(
                name=t["name"],
                defaults={
                    "role": t["role"],
                    "quote": t["quote"],
                    "rating": t["rating"],
                    "avatar_url": t["avatar"],
                    "featured": True,
                },
            )

        NewsletterSubscriber.objects.get_or_create(
            email="news@traveloop.demo",
            defaults={"active": True},
        )

        self.stdout.write(self.style.SUCCESS("Seed complete. Run the server and explore!"))
