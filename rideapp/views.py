from .models import CustomUser, Ride, Rider, Feedback
from .forms import CustomUserCreationForm, NicknameChangeForm, PhoneChangeForm, PhotoChangeForm, NewRideForm, JoinRequestForm, FeedbackForm, NewRideForm2, ProfileSetupForm
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.conf import settings
from twilio.rest import Client
from datetime import datetime
import geopy.distance
from geopy.geocoders import Nominatim
from django.utils import timezone
import copy

# from stackoverflow.com/questions/48642075/position-between-two-lat-long-coordinates-in-python
def find_point(a,b,alpha = 0.5):
    assert(0<=alpha<=1)
    new_a = ((1-alpha) * a[0], (1-alpha)*a[1])
    new_b = ((alpha) * b[0], alpha*b[1])
    return [(new_a[0]+new_b[0]), (new_a[1]+new_b[1])]

def message(target, message):
    account_sid = settings.TWILIO_ACCOUNT_SID
    auth_token = settings.TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    message = client.messages \
                    .create(
                        body="Hi " + target.first_name + ", " + message,
                        from_='+12568530059',
                        to='+1'+str(target.phone_number).replace('(','').replace(')','').replace('-','').replace(' ','')
                    )

    print(message.sid)

def reverseSearch(coords):
    #cod = coords.deconstruct()[2]
    geolocator = Nominatim(user_agent="http://127.0.0.1:8000")
    location = geolocator.reverse(coords, language='en')
    #print(location.address)
    #print(type(location.address))
    return location.address
    
def generalLoc(coords):
    geolocator = Nominatim(user_agent="http://127.0.0.1:8000")
    location = geolocator.reverse(coords, language='en')
    loc_dict = location.raw
    add = loc_dict['address']
    print(add)
    try:
        ret = add['building']
    except:
        try:
            ret = add['hamlet']
        except:
            try:
                ret = add['suburb']
            except:
                try:
                    ret = add['city']
                except:
                    ret = add['county']
    ret2 = add['state']
    return ret + ', ' + ret2

# Create your views here.

class HomePageView(TemplateView):
    #Ride.objects.all().filter(rideEndLoc=None).delete()
    template_name = 'home.html'

class SignUpView(CreateView):
    #Ride.objects.all().filter(rideEndLoc=None).delete()
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

@login_required
def NicknameChangeView(request):
    #Ride.objects.all().filter(rideEndLoc=None).delete()
    current_user = request.user
    if request.method == 'POST':
        form = NicknameChangeForm(request.POST)
        if form.is_valid():
            current_user.venmo_id = form.cleaned_data['venmo_id']
            current_user.save()
            return HttpResponseRedirect(reverse('profile'))
    else:
        proposed_name = ""
        form = NicknameChangeForm(initial={'last_name': proposed_name})

    context = {
    'form': form,
    'current_user': current_user,
    }
    return render(request, 'change_form.html', context)
    
@login_required
def ProfileSetupView(request):
    current_user = request.user
    if request.method == 'POST':
        form = ProfileSetupForm(request.POST)
        if form.is_valid():
            current_user.phone_number = form.cleaned_data['phone_number']
            current_user.save()
            return HttpResponseRedirect(reverse('ride-list'))
    else:
        proposed_name = ""
        form = ProfileSetupForm(initial={'last_name': proposed_name})

    context = {
    'form': form,
    'current_user': current_user,
    }
    return render(request, 'rideapp/profilesetup.html', context)
    
@login_required
def PhoneChangeView(request):
    #Ride.objects.all().filter(rideEndLoc=None).delete()
    current_user = request.user
    if request.method == 'POST':
        form = PhoneChangeForm(request.POST)
        if form.is_valid():
            current_user.phone_number = form.cleaned_data['phone_number']
            current_user.save()
            return HttpResponseRedirect(reverse('profile'))
    else:
        proposed_name = ""
        form = PhoneChangeForm(initial={'last_name': proposed_name})

    context = {
    'form': form,
    'current_user': current_user,
    }
    return render(request, 'change_form.html', context)
    
@login_required
def PhotoChangeView(request):
    #Ride.objects.all().filter(rideEndLoc=None).delete()
    current_user = request.user
    if request.method == 'POST':
        form = PhotoChangeForm(request.POST)
        if form.is_valid():
            current_user.photo = request.FILES['photo']
            current_user.save()
            return HttpResponseRedirect(reverse('profile'))
    else:
        proposed_name = "default.jpg"
        form = PhotoChangeForm(initial={'photo': proposed_name})

    context = {
    'form': form,
    'current_user': current_user,
    }
    return render(request, 'change_form.html', context)


@login_required
def ridelistView(request):
    if request.user.first_login == 0:
        request.user.first_login = 1
        request.user.save()
        return redirect('profilesetup')
    #Ride.objects.all().filter(rideEndLoc=None).delete()
    #Ride.objects.all().delete()
    posts = Ride.objects.all().order_by('-postedTime')
    context = {
        'posts' : posts
    }
    return render(request, 'rideapp/ridelist.html', context)
    

def aboutView(request):
    #Ride.objects.all().filter(rideEndLoc=None).delete()
    return render(request, 'rideapp/about.html')

@login_required
def feedbackView(request,ride_id):
    #Ride.objects.all().filter(rideEndLoc=None).delete()
    the_ride = get_object_or_404(Ride, pk=ride_id)
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            current_feedback = form.save(commit=False)
            current_feedback.driver = the_ride.driver
            current_feedback.ride = the_ride
            current_feedback.driver.avg_rating = str(round(((current_feedback.driver.count)*(current_feedback.driver.avg_rating)+int(current_feedback.rating))/(current_feedback.driver.count+1),2))
            current_feedback.driver.count += 1
            #current_feedback.driver.feedback.add(current_feedback.feedback)
            current_feedback.postTime = datetime.now()
            current_feedback.driver.save()
            current_feedback.save()
            return HttpResponseRedirect(reverse('ride-list'))
    else:
        form = FeedbackForm()
    return render(request, 'rideapp/feedback.html', {'form': form})
    
    
@login_required
def profileView(request):
    #Ride.objects.all().filter(rideEndLoc=None).delete()
    if Feedback.objects.filter(driver=request.user).count() > 0:
        feedbacks = Feedback.objects.filter(driver=request.user)
    else:
        feedbacks = []
        
    rat = round(request.user.avg_rating)
       
    filled = []
    not_filled = []
    there = True
       
    for i in range(rat):
        filled.append(rat)
           
    for i in range(5-rat):
        not_filled.append(rat)
       
    if Feedback.objects.filter(driver=request.user).count() > 0:
        feed = Feedback.objects.filter(driver=request.user)
    else:
        feed = []
        there = False
    total = 1
    if there:
        total = feed.count()
    fives = 0
    fours = 0
    threes = 0
    twos = 0
    ones = 0
    
    if there:
        for obj in feed:
            if obj.rating == 5:
                fives += 1
            if obj.rating == 4:
                fours += 1
            if obj.rating == 3:
                threes += 1
            if obj.rating == 2:
                twos += 1
            if obj.rating == 1:
                ones += 1
       
    len_5 = str(round(fives/total*100)) + "%"
    len_4 = str(round(fours/total*100)) + "%"
    len_3 = str(round(threes/total*100)) + "%"
    len_2 = str(round(twos/total*100)) + "%"
    len_1 = str(round(ones/total*100)) + "%"
    
    context = {
        'feedbacks' : feedbacks,
        'filled':filled,
        'not_filled':not_filled,
        'len_5':len_5,
        'len_4':len_4,
        'len_3':len_3,
        'len_2':len_2,
        'len_1':len_1,
        'fives' : fives,
        'fours' : fours,
        'threes' : threes,
        'twos' : twos,
        'ones' : ones,
    }
    
    return render(request, 'rideapp/profile.html',context)
    
    
@login_required
def RideFormView(request):
    #Ride.objects.all().filter(rideEndLoc=None).delete()
    current_ride = None
    if request.method == 'POST':
        form = NewRideForm(request.POST)
        if form.is_valid():
            current_ride = form.save(commit=False)
            current_ride.postedTime = timezone.now()
            current_ride.startAddress = reverseSearch(current_ride.rideStartLoc)
            current_ride.driver = request.user
            current_ride.save()
            return HttpResponseRedirect(reverse('addride2', args=(current_ride.id,)))
        else:
            g = form._errors
            form = NewRideForm()
            form._errors = g
    else:
        form = NewRideForm()
        #print("\n")
        #print(form.errors)
        #print("\n")

    context = {
    'form': form,
    'current_user': current_ride,
    }
    return render(request, 'rideapp/add_ride.html', context)
    
@login_required
def RideFormView2(request, ride_id):
    current_ride = get_object_or_404(Ride, pk=ride_id)
    if request.method == 'POST':
        form = NewRideForm2(request.POST)
        if form.is_valid():
            helper = form.save(commit=False)
            current_ride.postedTime = timezone.now()
            current_ride.rideEndLoc = helper.rideEndLoc
            current_ride.endAddress = reverseSearch(helper.rideEndLoc)
            current_ride.spacesAvailable = helper.spacesAvailable
            current_ride.cost = helper.cost
            current_ride.details = helper.details
            current_ride.generalDest = generalLoc(helper.rideEndLoc)
            current_ride.save()
            #message(current_ride.driver,"you posted a ride dummy")
            return HttpResponseRedirect(reverse('ride-list'))
        else:
            g = form._errors
            form = NewRideForm2()
            form._errors = g
    else:
        proposed_name = ""
        form = NewRideForm2(initial={'last_name': proposed_name})

    context = {
    'form': form,
    'current_user': current_ride,
    }
    return render(request, 'rideapp/add_ride2.html', context)

@login_required
def ridepage(request, ride_id, message=''):
    #Ride.objects.all().filter(rideEndLoc=None).delete()
    ride = get_object_or_404(Ride, pk=ride_id)
    alreadyIn = ride.riderList.filter(user=request.user).count()
    alreadyRequested = ride.riderRequests.all().filter(user=request.user).count()
    print(type(ride.rideStartLoc[0]))
    
    start = str(ride.rideStartLoc).replace('(','').replace(')','').split(',')
    startLoc = [float(i) for i in start]
    startLoc.reverse()
    end = str(ride.rideEndLoc).replace('(','').replace(')','').split(',')
    endLoc = [float(i) for i in end]
    endLoc.reverse()
    centerLoc = find_point(startLoc,endLoc) #[(startLoc[0]+endLoc[0])/2, (startLoc[1]+endLoc[1])/2]
    #print(centerLoc)
    mapKey = settings.MAPBOX_KEY
    
    #print("\n")
    #print(geopy.distance.vincenty(ride.rideStartLoc, ride.rideEndLoc).m)
    #print("\n")
    #generalLoc(ride.rideEndLoc)
    #generalLoc(ride.rideStartLoc)
    #print(startLoc)
    #print(endLoc)
    context = {
    'ride': ride,
    'alreadyIn': alreadyIn,
    'alreadyRequested': alreadyRequested,
    'startLoc': startLoc,
    'endLoc': endLoc,
    'mapKey': mapKey,
    'centerLoc': centerLoc,
    }
    return render(request, 'rideapp/ridepage.html', context)
    
@login_required
def myDrivesView(request):
    #Ride.objects.all().filter(rideEndLoc=None).delete()
    posts = Ride.objects.filter(driver=request.user).order_by('-postedTime')
    context = {
        'posts' : posts
    }
    return render(request, 'rideapp/mydrives.html', context)

@login_required
def myRidesView(request):
    #Ride.objects.all().filter(rideEndLoc=None).delete()
    posts = Ride.objects.filter(riderList__user=request.user).order_by('-postedTime')
    context = {
        'posts' : posts
    }
    return render(request, 'rideapp/myrides.html', context)


@login_required
def myOldRidesView(request):
    #Ride.objects.all().filter(rideEndLoc=None).delete()
    posts = Ride.objects.filter(rideDate__lt=datetime.today())
    posts = posts.filter(Q(riderList__user=request.user) | Q(driver=request.user)).order_by('-postedTime')
    context = {
        'posts' : posts
    }
    return render(request, 'rideapp/myoldrides.html', context)
    
    
@login_required
def ride_list(request):
    #Ride.objects.all().filter(rideEndLoc=None).delete()
    filter = RideFilter(request.GET, queryset=Ride.object.all())
    return render(request, 'rideapp/user_list.html', {'filter': filter})
    
@login_required
def userView(request, user_username):
    #Ride.objects.all().filter(rideEndLoc=None).delete()
    user_requested = get_object_or_404(CustomUser, username=user_username)
    rat = round(user_requested.avg_rating)
    
    filled = []
    not_filled = []
    there = True
    
    for i in range(rat):
        filled.append(rat)
        
    for i in range(5-rat):
        not_filled.append(rat)
    
    if Feedback.objects.filter(driver=user_requested).count() > 0:
        feed = Feedback.objects.filter(driver=user_requested)
    else:
        feed = []
        there = False
    total = 1
    if there:
        total = feed.count()
    fives = 0
    fours = 0
    threes = 0
    twos = 0
    ones = 0

    if there:
        for obj in feed:
            if obj.rating == 5:
                fives += 1
            if obj.rating == 4:
                fours += 1
            if obj.rating == 3:
                threes += 1
            if obj.rating == 2:
                twos += 1
            if obj.rating == 1:
                ones += 1
    
    len_5 = str(round(fives/total*100)) + "%"
    len_4 = str(round(fours/total*100)) + "%"
    len_3 = str(round(threes/total*100)) + "%"
    len_2 = str(round(twos/total*100)) + "%"
    len_1 = str(round(ones/total*100)) + "%"
    
    context = {
    'user_requested': user_requested,
    'filled':filled,
    'not_filled':not_filled,
    'len_5':len_5,
    'len_4':len_4,
    'len_3':len_3,
    'len_2':len_2,
    'len_1':len_1,
    'fives' : fives,
    'fours' : fours,
    'threes' : threes,
    'twos' : twos,
    'ones' : ones,
    }
    
    return render(request, 'rideapp/userpage2.html', context)

@login_required
def RideRequestView(request, ride_id):
    #Ride.objects.all().filter(rideEndLoc=None).delete()
    current_rider = None
    ride_obj = get_object_or_404(Ride, id = ride_id)
    if ride_obj.riderList.filter(user=request.user).count():
        # console.log("exists")
        return render(request, 'rideapp/profile.html', context)
    if request.method == 'POST':
        riderform = JoinRequestForm(request.POST)
        if riderform.is_valid():
            current_rider=riderform.save(commit=False)
            current_rider.user= request.user
            current_rider.save()
            RequestHelper(ride_id,current_rider)
            return HttpResponseRedirect(reverse('ridepage',args=[ride_id]))
    else:
        riderform = JoinRequestForm()
    context = {
    'riderform': riderform,
    'current_rider': current_rider,
    }
    return render(request, 'rideapp/join_ride.html', context)

#Helper method for ride request view
def RequestHelper(ride_id, rider):
    #Ride.objects.all().filter(rideEndLoc=None).delete()
    ride_obj = get_object_or_404(Ride, id=ride_id)
    ride_obj.riderRequests.add(rider)
    ride_obj.save()
    m = str(rider.user.first_name)+" has requested to join your ride. Head over to your mydrives page to approve or reject them."
    try:
        message(ride_obj.driver,m)
    except:
        None

def ApproveRider(request,ride_id,rider_id):
    #Ride.objects.all().filter(rideEndLoc=None).delete()
    ride_obj = get_object_or_404(Ride, id=ride_id)
    rider_obj = get_object_or_404(Rider, id=rider_id)
    ride_obj.riderList.add(rider_obj)
    ride_obj.riderRequests.remove(rider_obj)
    ride_obj.spacesAvailable-=1
    ride_obj.save()
    m = str(ride_obj.driver.first_name)+" has approved you to join their ride. You can see your rides at your myrides page."
    try:
        message(rider_obj.user,m)
    except:
        None
    return redirect('/mydrives')

def DeclineRider(request,ride_id,rider_id):
    #Ride.objects.all().filter(rideEndLoc=None).delete()
    ride_obj = get_object_or_404(Ride, id=ride_id)
    rider_obj = get_object_or_404(Rider, id=rider_id)
    ride_obj.riderRequests.remove(rider_obj)
    ride_obj.save()
    m = str(ride_obj.driver.first_name)+" has declined your request to join their ride. Sorry!"
    try:
        message(rider_obj.user,m)
    except:
        None
    return redirect('/mydrives')

def RemoveRider(request,ride_id,rider_id):
    #Ride.objects.all().filter(rideEndLoc=None).delete()
    ride_obj = get_object_or_404(Ride, id=ride_id)
    rider_obj = get_object_or_404(Rider, id=rider_id)
    ride_obj.riderList.remove(rider_obj)
    ride_obj.spacesAvailable += 1
    ride_obj.save()
    m = str(ride_obj.driver.first_name)+" has removed you from their ride. You can see your rides at your myrides page."
    try:
        message(rider_obj.user,m)
    except:
        None
    return redirect('/mydrives')
    
def LeaveRide(request,ride_id):
    #Ride.objects.all().filter(rideEndLoc=None).delete()
    ride_obj = get_object_or_404(Ride, id=ride_id)
    rider_obj = ride_obj.riderList.get(user=request.user)
    ride_obj.riderList.remove(rider_obj)
    ride_obj.spacesAvailable += 1
    ride_obj.save()
    return redirect('/myrides')

def DeleteRide(request,ride_id):
    #Ride.objects.all().filter(rideEndLoc=None).delete()
    ride_obj = get_object_or_404(Ride, id=ride_id)
    #Loop through riders and notify?
    ride_obj.delete()
    m = "You've deleted the ride. You can see your ride at your mydrives page."
    try:
        message(ride_obj.driver,m)
    except:
        None
    return redirect('/mydrives')
