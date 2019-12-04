from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.contenttypes.fields import GenericRelation
from .models import CustomUser, Ride, Rider, Feedback
import datetime
from django_starfield import Stars

class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('username', 'email','first_name','last_name','venmo_id','phone_number','photo')

class NicknameChangeForm(forms.ModelForm):

    #nickname = forms.CharField(required=False)
    
    class Meta:
        model = CustomUser
        fields = ('venmo_id',)
        

class PhoneChangeForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('phone_number',)
 
 
class PhotoChangeForm(forms.ModelForm):

    class Meta:
        model = CustomUser
        fields = ('photo',)
        
class DateInput(forms.DateInput):
    input_type = 'date'
    
class TimeInput(forms.TimeInput):
    input_type = 'time'
        

class NewRideForm(forms.ModelForm):
    
    class Meta:
        model = Ride
        fields = ['rideDate','rideTime','rideStartLoc',]
        widgets = {
            'rideDate': DateInput(),
            'rideTime': TimeInput(),
        }
        
    def clean_rideTime(self):
        date = self.cleaned_data['rideDate']
        time = self.cleaned_data['rideTime']
        if (date == datetime.date.today() and datetime.datetime.now().time() > time):
            raise forms.ValidationError("The time cannot be in the past!")
        if date < datetime.date.today() or (date == datetime.date.today() and datetime.datetime.now().time() > time):
            raise forms.ValidationError("The date cannot be in the past! Please fix the date.")
        return time
        

class NewRideForm2(forms.ModelForm):

    class Meta:
        model = Ride
        fields = ['rideEndLoc', 'spacesAvailable', 'cost', 'details']
        widgets = {
            'rideDate': DateInput(),
            'rideTime': TimeInput(),
            'details': forms.Textarea(attrs={'rows': 3, 'cols': 45}),
        }
        
    def clean_spacesAvailable(self):
        spaces = self.cleaned_data['spacesAvailable']
        if spaces < 1:
            raise forms.ValidationError("You have to have at least one space! Otherwise what's the point of posting a ride...")
        return spaces


class JoinRequestForm(forms.ModelForm):
    class Meta:
        model = Rider
        fields = ['pickupLoc', 'dropoffLoc', 'additionalNotes']
        
class FeedbackForm(forms.ModelForm):

    class Meta:
        model = Feedback
        fields = ['rating', 'feedback']
        widgets = {
            'feedback': forms.Textarea(attrs={'rows': 3, 'cols': 45}),
            'rating': Stars,
        }

class ProfileSetupForm(forms.ModelForm):

#nickname = forms.CharField(required=False)

    class Meta:
        model = CustomUser
        fields = ('phone_number',)
