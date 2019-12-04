from django.urls import path
from django.conf.urls import url
from django_filters.views import FilterView
from .filters import RideFilter

from . import views

urlpatterns = [
    path('ridelist', views.ridelistView, name='ride-list'),
    path('about', views.aboutView, name='about'),
    path('', views.HomePageView.as_view(), name='home'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('nicknamechange/', views.NicknameChangeView, name='nicknamechange'),
    path('phonechange/', views.PhoneChangeView, name='phonechange'),
    path('photochange/', views.PhotoChangeView, name='photochange'),
    path('addride/', views.RideFormView, name='addride'),
    path('addride2/<int:ride_id>', views.RideFormView2, name='addride2'),
    path('profile/', views.profileView, name='profile'),
    path('<int:ride_id>/ridepage/', views.ridepage, name='ridepage'),
    path('<str:user_username>/info', views.userView, name='userview'),
    path('myrides/', views.myRidesView, name='myrides'),
    path('<int:ride_id>/ridepage/riderequests/', views.RideRequestView, name='joinRide'),
    path('mydrives/', views.myDrivesView, name='mydrives'),
    path('mydrives/+/<int:ride_id>/<int:rider_id>', views.ApproveRider, name='addrider'),
    path('mydrives/-/<int:ride_id>/<int:rider_id>', views.DeclineRider, name='declinerider'),
    path('mydrives/remove/<int:ride_id>/<int:rider_id>', views.RemoveRider, name='declinerider'),
    path('myoldrides/', views.myOldRidesView, name='myoldrides'),
    url(r'^search/$', FilterView.as_view(filterset_class=RideFilter,template_name='rideapp/user_list.html'), name='search'),
    path('<int:ride_id>/feedback/', views.feedbackView, name='feedback'),
    path('mydrives/leave/<int:ride_id>', views.LeaveRide, name='leaveride'),
    path('mydrives/remove/<int:ride_id>/<int:rider_id>', views.RemoveRider, name='removerider'),
    path('mydrives/delete/<int:ride_id>', views.DeleteRide, name='deleteride'),
    path('profilesetup/', views.ProfileSetupView, name='profilesetup'),
]
