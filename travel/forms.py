"""Forms used by Traveloop planner flows."""
from datetime import timedelta

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import Activity, Budget, CityStop, Note, PackingItem, Trip, UserProfile

User = get_user_model()
CTRL = "form-control"


# travel/forms.py

# Replace the StyledLoginForm and SignUpForm classes

class StyledLoginForm(AuthenticationForm):
    def __init__(self, request=None, *args, **kwargs):
        super().__init__(request=request, *args, **kwargs)
        self.fields["username"].label = "Email"
        self.fields["username"].widget.attrs.update({
            "class": CTRL, 
            "autofocus": True,
            "placeholder": "email@example.com"
        })
        self.fields["password"].widget.attrs.update({"class": CTRL, "placeholder": "Enter your password"})

class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=120, required=False)
    last_name = forms.CharField(max_length=120, required=False)

    class Meta:
        model = User
        fields = ("email", "first_name", "last_name", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({"class": CTRL})
        self.fields["email"].widget.attrs.update({"placeholder": "email@example.com"})
        self.fields["first_name"].widget.attrs.update({"placeholder": "Jane"})
        self.fields["last_name"].widget.attrs.update({"placeholder": "Doe"})
        self.fields["password1"].widget.attrs.update({"placeholder": "Create a secure password"})
        self.fields["password2"].widget.attrs.update({"placeholder": "Confirm your password"})

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.username = self.cleaned_data["email"] # Email as username
        user.first_name = self.cleaned_data.get("first_name", "")
        user.last_name = self.cleaned_data.get("last_name", "")
        if commit:
            user.save()
            UserProfile.objects.get_or_create(user=user)
        return user
    
class TripForm(forms.ModelForm):
    class Meta:
        model = Trip
        fields = ["title", "description", "start_date", "end_date", "cover_image", "is_public"]
        widgets = {
            "title": forms.TextInput(attrs={"class": CTRL, "placeholder": "e.g., Summer in Europe"}),
            "description": forms.Textarea(attrs={"rows": 4, "class": CTRL, "placeholder": "Add any goals, ideas, or notes about this trip..."}),
            "start_date": forms.DateInput(attrs={"type": "date", "class": CTRL, "placeholder": "YYYY-MM-DD"}),
            "end_date": forms.DateInput(attrs={"type": "date", "class": CTRL, "placeholder": "YYYY-MM-DD"}),
            "cover_image": forms.ClearableFileInput(attrs={"class": CTRL}),
            "is_public": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean(self):
        cleaned = super().clean()
        start_date = cleaned.get("start_date")
        end_date = cleaned.get("end_date")
        if start_date and end_date and end_date < start_date:
            raise ValidationError("End date cannot be before start date.")
        return cleaned


class CityStopForm(forms.ModelForm):
    class Meta:
        model = CityStop
        fields = ["city_name", "country", "arrival_date", "departure_date", "order"]
        widgets = {
            "city_name": forms.TextInput(attrs={"class": CTRL, "placeholder": "e.g., Paris"}),
            "country": forms.TextInput(attrs={"class": CTRL, "placeholder": "e.g., France"}),
            "arrival_date": forms.DateInput(attrs={"type": "date", "class": CTRL, "placeholder": "YYYY-MM-DD"}),
            "departure_date": forms.DateInput(attrs={"type": "date", "class": CTRL, "placeholder": "YYYY-MM-DD"}),
            "order": forms.NumberInput(attrs={"class": CTRL, "min": 1, "placeholder": "e.g., 1"}),
        }

    def clean(self):
        cleaned = super().clean()
        arrival = cleaned.get("arrival_date")
        departure = cleaned.get("departure_date")
        if arrival and departure and departure < arrival:
            raise ValidationError("Departure date cannot be before arrival date.")
        return cleaned


class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = [
            "city_stop",
            "title",
            "category",
            "description",
            "cost",
            "duration_hours",
            "activity_date",
        ]
        widgets = {
            "city_stop": forms.Select(attrs={"class": CTRL}),
            "title": forms.TextInput(attrs={"class": CTRL, "placeholder": "e.g., Eiffel Tower Visit"}),
            "category": forms.Select(attrs={"class": CTRL}),
            "description": forms.Textarea(attrs={"rows": 3, "class": CTRL, "placeholder": "Reservation details, opening hours, etc."}),
            "cost": forms.NumberInput(attrs={"class": CTRL, "step": "0.01", "min": "0", "placeholder": "e.g., 50.00"}),
            "duration_hours": forms.NumberInput(attrs={"class": CTRL, "step": "0.5", "min": "0", "placeholder": "e.g., 2.5"}),
            "activity_date": forms.DateInput(attrs={"type": "date", "class": CTRL, "placeholder": "YYYY-MM-DD"}),
        }


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = [
            "transport_cost",
            "hotel_cost",
            "food_cost",
            "activity_cost",
            "miscellaneous_cost",
        ]
        widgets = {
            "transport_cost": forms.NumberInput(attrs={"class": CTRL, "step": "0.01", "min": "0", "placeholder": "0.00"}),
            "hotel_cost": forms.NumberInput(attrs={"class": CTRL, "step": "0.01", "min": "0", "placeholder": "0.00"}),
            "food_cost": forms.NumberInput(attrs={"class": CTRL, "step": "0.01", "min": "0", "placeholder": "0.00"}),
            "activity_cost": forms.NumberInput(attrs={"class": CTRL, "step": "0.01", "min": "0", "placeholder": "0.00"}),
            "miscellaneous_cost": forms.NumberInput(attrs={"class": CTRL, "step": "0.01", "min": "0", "placeholder": "0.00"}),
        }


class PackingItemForm(forms.ModelForm):
    class Meta:
        model = PackingItem
        fields = ["item_name", "category"]
        widgets = {
            "item_name": forms.TextInput(attrs={"class": CTRL, "placeholder": "e.g., Passport"}),
            "category": forms.Select(attrs={"class": CTRL}),
        }


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"class": CTRL, "placeholder": "e.g., Flight Details"}),
            "content": forms.Textarea(attrs={"rows": 4, "class": CTRL, "placeholder": "Enter your notes here..."}),
        }


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(max_length=120, required=False)
    last_name = forms.CharField(max_length=120, required=False)
    email = forms.EmailField(required=True)

    class Meta:
        model = UserProfile
        fields = ["avatar", "phone", "bio", "preferred_travel_style", "language_preference"]
        widgets = {
            "phone": forms.TextInput(attrs={"class": CTRL, "placeholder": "+1 (555) 000-0000"}),
            "bio": forms.Textarea(attrs={"rows": 3, "class": CTRL, "placeholder": "Tell us a bit about yourself and your travel style..."}),
            "preferred_travel_style": forms.TextInput(attrs={"class": CTRL, "placeholder": "e.g., Backpacker, Luxury, Adventure"}),
            "avatar": forms.ClearableFileInput(attrs={"class": CTRL}),
            "language_preference": forms.Select(attrs={"class": CTRL}),
        }

    def __init__(self, *args, user=None, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({"class": CTRL, "placeholder": "Jane"})
        self.fields["last_name"].widget.attrs.update({"class": CTRL, "placeholder": "Doe"})
        self.fields["email"].widget.attrs.update({"class": CTRL, "placeholder": "email@example.com"})
        if user:
            self.fields["first_name"].initial = user.first_name
            self.fields["last_name"].initial = user.last_name
            self.fields["email"].initial = user.email

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        qs = User.objects.filter(email__iexact=email).exclude(pk=self.user.pk)
        if qs.exists():
            raise ValidationError("This email is already used by another account.")
        return email

    def save(self, commit=True):
        profile = super().save(commit=False)
        self.user.first_name = self.cleaned_data["first_name"]
        self.user.last_name = self.cleaned_data["last_name"]
        self.user.email = self.cleaned_data["email"]
        if commit:
            self.user.save()
            profile.save()
        return profile


class SearchForm(forms.Form):
    q = forms.CharField(required=False, label="Keyword")
    start = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date", "class": CTRL, "placeholder": "YYYY-MM-DD"}))
    end = forms.DateField(required=False, widget=forms.DateInput(attrs={"type": "date", "class": CTRL, "placeholder": "YYYY-MM-DD"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["q"].widget.attrs.update({"class": CTRL, "placeholder": "Search city, country, activity"})

    def clean(self):
        cleaned = super().clean()
        start = cleaned.get("start")
        end = cleaned.get("end")
        if start and end and end < start:
            raise ValidationError("End date cannot be before start date.")
        if start and start < timezone.localdate() - timedelta(days=3650):
            raise ValidationError("Start date looks invalid.")
        return cleaned

from .models import Booking

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ["travel_date", "travelers_count"]
        widgets = {
            "travel_date": forms.DateInput(attrs={"type": "date", "class": CTRL, "placeholder": "YYYY-MM-DD"}),
            "travelers_count": forms.NumberInput(attrs={"class": CTRL, "min": 1, "id": "id_travelers_count", "placeholder": "e.g., 2"}),
        }
