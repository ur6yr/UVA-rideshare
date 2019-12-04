from django.test import TestCase
from .models import CustomUser, Ride
import datetime
from django.utils import timezone
from django.urls import reverse
from django.test import Client

# Create your tests here.
# login tests help from stackoverflow.com/questions/2705235/django-test-failing-on-a-view-with-login-required

def create_user(username, password, email, first_name, last_name):
    return CustomUser.objects.create(username=username,password=password,email=email, first_name=first_name, last_name=last_name)
    
def create_ride(postedTime, rideDate, rideTime, rideEndLoc, spacesAvailable):
    return Ride.objects.create(postedTime=postedTime, rideDate=rideDate, rideTime=rideTime, rideEndLoc=rideEndLoc, spacesAvailable=spacesAvailable)

class UserTests(TestCase):
    def test_first_name(self):
    #Check that user fields are set correctly when user created
        test_user = create_user("test","test","test_email@virginia.edu", "Test", "User")
        self.assertEqual(test_user.first_name,"Test")
        
    def test_email(self):
    #Check that user fields are set correctly when user created
        test_user = create_user("test","test","test_email@virginia.edu", "Test", "User")
        self.assertEqual(test_user.email,"test_email@virginia.edu")
        
    def test_last_name(self):
    #Check that user fields are set correctly when user created
        test_user = create_user("test","test","test_email@virginia.edu", "Test", "User")
        self.assertEqual(test_user.last_name, "User")
        
class RideTests(TestCase):
    def test_was_published_recently_old(self):
        time = timezone.now() - datetime.timedelta(days=1,seconds=1)
        old_ride = Ride(postedTime=time)
        self.assertIs(old_ride.was_published_recently(),False)
        
    def test_was_published_recently_new(self):
        time = timezone.now() - datetime.timedelta(hours=23,minutes=59,seconds=59)
        recent_ride = Ride(postedTime=time)
        self.assertIs(recent_ride.was_published_recently(),True)
    
    def test_ride_date(self):
        ride = Ride(rideDate=datetime.datetime.now())
        self.assertIs(ride.has_rideDate(),True)
        
    def test_ride_time(self):
        ride = Ride(rideTime=datetime.datetime.now())
        self.assertIs(ride.has_rideTime(),True)
        
        
class HomeViewTests(TestCase):
    def test_home_not_404(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        
class AboutViewTests(TestCase):
    def test_about_not_404(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        
class RideListViewFirstLoginTests(TestCase):
    def test_ridelist_not_404(self):
        response = self.client.get(reverse('ride-list'))
        self.assertEqual(response.status_code, 302)
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    def test_ridelist_not_404_first_login(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('ride-list'))
        self.assertEqual(response.status_code, 302)
    def test_ridelist_not_404_redirect_setup(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('ride-list'))
        self.assertRedirects(response,'/profilesetup/', status_code=302,target_status_code=200, msg_prefix='', fetch_redirect_response=True)

class RideListViewTests(TestCase):
    def test_ridelist_not_404(self):
        response = self.client.get(reverse('ride-list'))
        self.assertEqual(response.status_code, 302)
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    def test_ridelist_not_404_login(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('ride-list'))
        response = self.client.get(reverse('profile'))
        response = self.client.get(reverse('ride-list'))
        self.assertEqual(response.status_code, 200)

class MyRidesViewTests(TestCase):
    def test_myrides_not_404(self):
        response = self.client.get(reverse('myrides'))
        self.assertEqual(response.status_code, 302)
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    def test_myrides_not_404_login(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('myrides'))
        self.assertEqual(response.status_code, 200)
        
class AddRideViewTests(TestCase):
    def test_addride_not_404(self):
        response = self.client.get(reverse('addride'))
        self.assertEqual(response.status_code, 302)
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    def test_addride_not_404_login(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('addride'))
        self.assertEqual(response.status_code, 200)
    
        
class LoginViewTests(TestCase):
    def test_login_not_404(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        
class ProfileViewTests(TestCase):
    def test_profile_not_404(self):
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    def test_profile_not_404_login(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        
class UserViewTests(TestCase):
    def test_userpage_not_404(self):
        test_user = create_user("test","test","test_email@virginia.edu", "Test", "User")
        response = self.client.get(reverse('userview',args=(test_user.id,)))
        self.assertEqual(response.status_code, 302)
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    def test_userpage_not_404_login(self):
        self.client.login(username='john', password='johnpassword')
        test_user = create_user("test","test","test_email@virginia.edu", "Test", "User")
        response = self.client.get(reverse('userview',args=(test_user.username,)))
        self.assertEqual(response.status_code, 200)
        
class RidePageViewTests(TestCase):
    def test_ridepage_not_404(self):
        ride = create_ride(timezone.now(),datetime.datetime.now(),datetime.datetime.now(),'there',2)
        response = self.client.get(reverse('ridepage',args=(ride.id,)))
        self.assertEqual(response.status_code, 302)

class PhoneChangeViewTests(TestCase):
    def test_phonechange_not_404(self):
        response = self.client.get(reverse('phonechange'))
        self.assertEqual(response.status_code, 302)
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    def test_phonechange_not_404_login(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('phonechange'))
        self.assertEqual(response.status_code, 200)
        
class PhotoChangeViewTests(TestCase):
    def test_photochange_not_404(self):
        response = self.client.get(reverse('photochange'))
        self.assertEqual(response.status_code, 302)
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    def test_photochange_not_404_login(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('photochange'))
        self.assertEqual(response.status_code, 200)
        
class NicknameChangeViewTests(TestCase):
    def test_nickname_not_404(self):
        response = self.client.get(reverse('nicknamechange'))
        self.assertEqual(response.status_code, 302)
    def setUp(self):
        self.client = Client()
        self.user = CustomUser.objects.create_user('john', 'lennon@thebeatles.com', 'johnpassword')
    def test_nickname_not_404_login(self):
        self.client.login(username='john', password='johnpassword')
        response = self.client.get(reverse('nicknamechange'))
        self.assertEqual(response.status_code, 200)
        
class SignupViewTests(TestCase):
    def test_signup_not_404(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)

