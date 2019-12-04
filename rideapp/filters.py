#source: https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html
from .models import Ride
import django_filters
import datetime
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from datetime import date

class RideFilter(django_filters.FilterSet):
    
    startAddress = django_filters.CharFilter(lookup_expr='contains')
    endAddress = django_filters.CharFilter(lookup_expr='contains')
    rideTime = django_filters.TimeFilter(widget=forms.TimeInput(attrs={
        'type': 'time'
    }))
    # rideTime = django_filters.CharFilter(lookup_expr='contains')
    # rideDate = django_filters.CharFilter(lookup_expr='contains')
    rideDate = django_filters.DateFilter(widget=forms.DateInput(attrs={
        'type': 'date'
    }))
    class Meta:
        model = Ride
        fields =  [
                  'rideDate',
                  'rideTime',
                  # 'postedTime',
                  # 'rideStartLoc',
                  # 'rideEndLoc',
                  'startAddress',
                  'endAddress', #old: endAddress
                  # 'spacesAvailable',
                  # 'cost',
                  # 'driver'
                 ]
