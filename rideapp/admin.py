from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Ride, Rider, Feedback
from .forms import CustomUserCreationForm, NicknameChangeForm, PhoneChangeForm
from mapbox_location_field.admin import MapAdmin

# Register your models here.

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = PhoneChangeForm
    form = NicknameChangeForm

admin.site.register(CustomUser) #,CustomUserAdmin)
admin.site.register(Ride, MapAdmin)
admin.site.register(Rider)
admin.site.register(Feedback)
