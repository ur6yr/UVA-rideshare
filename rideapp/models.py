from django.db import models
from django.contrib.auth.models import AbstractUser
from djmoney.models.fields import MoneyField
from phone_field import PhoneField
import datetime
from django.utils import timezone
from mapbox_location_field.models import LocationField, AddressAutoHiddenField
from django.contrib.contenttypes.fields import GenericRelation
from djmoney.models.validators import MaxMoneyValidator, MinMoneyValidator
# Create your models here.
class CustomUser(AbstractUser):
    venmo_id = models.CharField(max_length=200, default='')
    phone_number = PhoneField(E164_only=True)
    photo = models.ImageField(upload_to='images/',default='images/default.jpg')
    avg_rating = models.FloatField(default=0.0)
    count = models.IntegerField(default=0)
    first_login = models.IntegerField(default=0)
    @property
    def full_name(self):
        return '{} {}'.format(self.first_name, self.last_name)

class Rider(models.Model):
    user =  models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    pickupLoc = models.CharField('Pick Up Location', max_length=200)
    dropoffLoc = models.CharField('Drop Off Location', max_length=200)
    additionalNotes = models.CharField('Additional Notes', max_length=500)

class Ride(models.Model):
    # id = serial number
    postedTime = models.DateTimeField('Posted Date')
    rideDate = models.DateField('Ride Date')
    rideTime = models.TimeField('Ride Departure Time:')
    rideStartLoc = LocationField('Departure location',map_attrs={'center': [38.034887,-78.504832], 'marker_color': 'blue','placeholder': 'Pick a location below'}, null=True)
    startAddress = models.CharField('Start location',max_length=500, default='')
    rideEndLoc = LocationField('Destination',map_attrs={'center': [38.034887,-78.504832], 'marker_color': 'blue'}, null=True)
    endAddress = models.CharField(max_length=500, default='')
    generalDest = models.CharField(max_length=500, default='')
    riderRequests = models.ManyToManyField(Rider, related_name='+')
    riderList = models.ManyToManyField(Rider, related_name='+')
    spacesAvailable = models.IntegerField('Spaces Available',default=0)
    cost = MoneyField(decimal_places=2, default=0, max_digits=5, default_currency='USD', validators=[MinMoneyValidator(0), MaxMoneyValidator(1000)])
    details = models.TextField('Additional details for riders (optional)', blank = True, default ='')
    driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    #feedback = models.ManyToManyField("self")

    def feedback_list(self):
        return list(self.feedback.all())
    
    def was_published_recently(self):
        return self.postedTime >= timezone.now() - datetime.timedelta(days=1)
        
    def has_rideDate(self):
        return self.rideDate != None
        
    def has_rideTime(self):
        return self.rideTime != None
        
    def has_rideTime(self):
        return self.rideTime != None

    def in_past(self):
        return (self.rideDate < datetime.date.today())

    def is_current(self):
        return (self.rideDate > datetime.date.today() or (self.rideTime > datetime.datetime.now().time() and self.rideDate == datetime.date.today()))

    def has_space(self):
        return (self.spacesAvailable > 0)

    def has_endLoc(self):
        return self.rideEndLoc != None
    
    def __str__(self):  # __unicode__ on Python 2
        return (self.generalDest)


class Feedback(models.Model):
    rating = models.IntegerField(default=5)
    feedback = models.TextField(default='')
    driver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True)
    ride = models.ForeignKey(Ride, on_delete=models.CASCADE, null=True)

