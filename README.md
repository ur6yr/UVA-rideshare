[![Build Status](https://travis-ci.com/ur6yr/UVA-rideshare.svg?branch=master)](https://travis-ci.com/ur6yr/UVA-rideshare)
# AQUAE Rideshare
This app is live on Heroku at this [link](http://aquae.herokuapp.com/)

The AQUAE team (**A**nna, **Q**uincy, **U**ttam, **A**rty, and **E**dward) created a rideshare web application using the Django web framework, with GitHub as our
source control management, Travis CI to manage our continuous integration, and Heroku as our cloud hosting
service. Below are details of the functionality of the app, resources used, and other notes.

## Table of contents
* [Video](#Video-showing-functionality)
* [Homepage](#Homepage)
* [About page](#About-page)
* [Login](#Login)
* [Ride listing page and Search](#Ride-listing-page-and-Search)
* [Ride information pages](#Ride-information-pages)
* [Profile and user pages](#Profile-and-user-pages)
* [My rides pages](#My-rides-pages)
* [Create a ride](#Create-a-ride)
* [Notifications](#Notifications)
* [Sources and used libraries](#Sources-and-used-libraries)
  * [Installed libraries](#Installed-libraries)
  * [Tutorials used](#Tutorials-used)
  * [Note on code usage](#Note-on-code-usage)
* [Testing](#Testing)
* [Other notes](#Other-notes)

## Video showing functionality
[Video link](https://youtu.be/6pxzL1qdL9Y)

This video pretty much shows the basic functionality of the application.

## Homepage
On the homepage there is drone footage of UVA and a quick explanation of the app. Additionally, there is Drift chat bot for any questions
that users might have.

## About page
There is an About page that users can access regardless or their login status. The About page provides references used in the app.

## Login
Clicking either Ride List or Login prompts the user to login. To login, the user must use their UVA email. Upon their first login, they 
will need to enter their phone number. Their phone number is required so that they can receive notifications about updates to their status
as a rider, and for drivers to know when they have requests from riders.

## Ride listing page and Search
The Ride List shows all of the available rides in the system. Past rides will not show on the Ride List. The user can browse the Ride List,
or click the Search for Rides button to filter the Ride List by date, departure time, starting location, and destination. 

## Ride information pages
The user can go to a ride page by clicking on the end location of a ride from the filter page or from the Ride List. The user can request
to join rides depending on the space available. The driver can see these requests from the subcategory “I’m Driving” under the “My Rides”
tab on the header. The driver can accept or reject a rider. Before doing so, the driver can look at a rider’s profile to determine if they
want to accept or reject.

## Profile and user pages
A user’s profile shows their name, profile picture, email, phone number, Venmo ID, and average rating to other users. A user can access
others’ profiles through links on a specific ride page. However, a user may always view their own profile using the “Profile” tab on the
header. A user’s own profile additionally shows the user any feedback they may have on a ride. Feedback may be given to drivers on past 
rides, after the ride has started. Feedback comes in the form of a rating and commentary. The ratings given are reflect on a user’s 
profile. Commentary is shown on the driver’s “My Past Trips” under the “My Rides” tab on the header, but is not public to all users.

## My rides pages
A user may view they rides they have been accepted to from “I’m Riding” under the “My Rides” tab on the header.  
A user may view they rides they are driving from “I’m Driving” under the “My Rides” tab on the header. 
A user may view their past rides (both riding and drving) from “My past trips” under the “My Rides” tab on the header.  

## Create a ride
A user may create a ride by clicking “Create Ride” on the header and completing the form. The user must specify the start location and 
end location using mapbox, the departure date and time, the number of spaces available, and the cost per rider. The user also has the 
opportunity to enter any additional details if they chose to do so.

## Notifications
A user receives text message notifications in the following situations: a rider requests to join a ride, a driver approves a rider, a 
driver removes a rider, or a driver deletes a ride.

## Sources and used libraries

### Installed libraries

#### django
*  Summary: A high-level Python Web framework that encourages rapid development and clean, pragmatic design.
*  Author: Django Software Foundation
*  Date: 12/1/19
*  Code version: 2.2.5
*  URL: https://www.djangoproject.com/
*  Software License: BSD

#### gunicorn
*  Summary: WSGI HTTP Server for UNIX
*  Author: Benoit Chesneau
*  Date: 12/1/19
*  Code version: 19.9.0
*  URL: http://gunicorn.org
*  Software License: MIT

#### django-heroku
*  Summary: This is a Django library for Heroku apps.
*  Author: Kenneth Reitz
*  Date: 12/1/19
*  Code version: 19.9.0
*  URL: https://github.com/heroku/django-heroku
*  Software License: MIT

#### django-crispy-forms
*  Summary: Best way to have Django DRY forms
*  Author: Miguel Araujo
*  Date: 12/1/19
*  Code version: 1.7.2
*  URL: http://github.com/maraujop/django-crispy-forms
*  Software License: MIT

#### django-allauth
*  Summary: Integrated set of Django applications addressing authentication, registration, account management as well as 3rd party (social) account authentication.
*  Author: Raymond Penners
*  Date: 12/1/19
*  Code version: 0.40.0
*  URL: http://github.com/pennersr/django-allauth
*  Software License: MIT

#### social-auth-app-django
*  Summary: Python Social Authentication, Django integration.
*  Author: Matias Aguirre
*  Date: 12/1/19
*  Code version: 3.1.0
*  URL: https://github.com/python-social-auth/social-app-django
*  Software License: BSD

#### Pillow
*  Summary: Python Imaging Library (Fork)
*  Author: Alex Clark (PIL Fork Author)
*  Date: 12/1/19
*  Code version: 6.2.1
*  URL: http://python-pillow.org
*  Software License: HPND

#### django-money
*  Summary: Adds support for using money and currency fields in django models and forms. Uses py-moneyed as the money implementation.
*  Author: Jacob Hansson
*  Date: 12/1/19
*  Code version: 0.15.1
*  URL: https://github.com/django-money/django-money
*  Software License: BSD

#### django-phone-field
*  Summary: Lightweight model and form field for phone numbers in Django
*  Author: Andrew Mackowski
*  Date: 12/1/19
*  Code version: 1.8.0
*  URL: https://github.com/VeryApt/django-phone-field/
*  Software License: GPL


#### django-phonenumber-field
*  Summary: An international phone number field for django models.
*  Author: Stefan Foulis
*  Date: 12/1/19
*  Code version: 3.0.1
*  URL: https://github.com/stefanfoulis/django-phonenumber-field
*  Software License: BSD

#### phonenumbers
*  Summary: An international phone number field for django models.
*  Author: David Drysdale
*  Date: 12/1/19
*  Code version: 8.10.21
*  URL: https://github.com/daviddrysdale/python-phonenumbers
*  Software License: Apache License 2.0

#### django-storages
*  Summary: Support for many storage backends in Django
*  Author: Josh Schneier
*  Date: 12/1/19
*  Code version: 1.7.2
*  URL: https://github.com/jschneier/django-storages
*  Software License: BSD

#### boto3
*  Summary: The AWS SDK for Python
*  Author: Amazon Web Services
*  Date: 12/1/19
*  Code version: 1.10.1
*  URL: https://github.com/boto/boto3
*  Software License: Apache License 2.0

#### django-mapbox-location-field
*  Summary: location field with MapInput widget for picking some location
*  Author: Szymon Kowaliński
*  Date: 12/1/19
*  Code version: 0.2.5
*  URL: https://github.com/Simon-the-Shark/django-mapbox-location-field
*  Software License: MIT

#### django-location-field
*  Summary: Location field for Django
*  Author: Caio Ariede
*  Date: 12/1/19
*  Code version: 2.1.0
*  URL: http://github.com/caioariede/django-location-field
*  Software License: MIT

#### geopy
*  Summary: Python Geocoding Toolbox
*  Author: GeoPy Contributors
*  Date: 12/1/19
*  Code version: 1.20.0
*  URL: https://github.com/geopy/geopy
*  Software License: MIT

#### twilio
*  Summary: Twilio API client and TwiML generator
*  Author: Twilio
*  Date: 12/1/19
*  Code version: 6.33.0
*  URL: https://github.com/twilio/twilio-python/
*  Software License: MIT

#### django-twilio
*  Summary: Build Twilio functionality into your Django apps.
*  Author: Randall Degges
*  Date: 12/1/19
*  Code version: 0.11.0
*  URL: https://github.com/rdegges/django-twilio
*  Software License: UNLICENSE

#### django-filter
*  Summary: Django-filter is a reusable Django application for allowing users to filter querysets dynamically.
*  Author: Alex Gaynor
*  Date: 12/1/19
*  Code version: 2.2.0
*  URL: https://github.com/carltongibson/django-filter/tree/master
*  Software License: BSD

#### django-bootstrap-form
*  Summary: django-bootstrap-form
*  Author: tzangms
*  Date: 12/1/19
*  Code version: 3.4
*  URL: http://github.com/tzangms/django-bootstrap-form
*  Software License: MIT

#### django-widget-tweaks
*  Summary: Tweak the form field rendering in templates, not in python-level form definitions.
*  Author: Mikhail Korobov
*  Date: 12/1/19
*  Code version: 1.4.5
*  URL: https://github.com/jazzband/django-widget-tweaks
*  Software License: MIT

#### django-starfield
*  Summary: A no-frills Django form widget for rating stars
*  Author: Dominik George
*  Date: 12/1/19
*  Code version: 1.0.post1
*  URL: https://edugit.org/nik/django-starfield
*  Software License: MIT

### Tutorials used
* [Setting up python virtual environment](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)
* [Using Boostrap 4 forms](https://simpleisbetterthancomplex.com/tutorial/2018/08/13/how-to-use-bootstrap-4-forms-with-django.html)
* [Configuring django for Heroku](https://devcenter.heroku.com/articles/deploying-python)
* [Google authentication in Django](https://fosstack.com/how-to-add-google-authentication-in-django/)
* [Restricting access](https://coderbook.com/@marcus/how-to-restrict-access-with-django-permissions/)
* [Image uploads and media root configuration](https://wsvincent.com/django-image-uploads/)
* [Styling images](https://www.w3schools.com/css/css3_images.asp)
* [Setup AWS s3 bucket for media files](https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/)
* [Geocoding with geopy](https://chrisalbon.com/python/data_wrangling/geocoding_and_reverse_geocoding/)
* [Drift bot](https://www.drift.com/messaging/)
* [Homepage video background](https://www.w3schools.com/howto/howto_css_fullscreen_video.asp)
* [Add twilio messaging](https://www.twilio.com/docs/sms/tutorials/server-notifications-python-django)
* [Making things responsive to screen size](https://redstapler.co/responsive-css-video-background/)
* [Style for user rating scorecard (no javascript)](https://www.w3schools.com/howto/howto_css_user_rating.asp)
* [Using Mapbox direction API](https://docs.mapbox.com/help/tutorials/getting-started-directions-api/)
* [Centering map between start and end locations](https://stackoverflow.com/questions/48642075/position-between-two-lat-long-coordinates-in-python)
* [Adding star picker for feedback](https://pypi.org/project/django-starfield/)
* [Understanding Django migrations and foreignkey columns](https://realpython.com/digging-deeper-into-migrations/)
* [General theme and template](https://www.youtube.com/playlist?list=PL-osiE80TeTtoQCKZ03TU5fNfx2UY6U4p)
* [Tutorial for djang-filter](https://www.bedjango.com/blog/how-use-django-filter/)
* [Another tutorial for filtering queryset](https://simpleisbetterthancomplex.com/tutorial/2016/11/28/how-to-filter-querysets-dynamically.html)

### Note on code usage
If code was copied and modified from stackoverflow or other sites it is cited in the file it is used in. There should only be three places where this is the case. 1) The Mapbox display on each individual ridepage which was heavily modified to work for our site. 2) The rating scorecard css and html which was also heavily modified to use javascript and Django template langauge to update the ratings and make the bars move instead of being static. 3) The code to find the center between two lat and lang points on a map.

## Testing
We have 31 tests written which cover each view of our app. These inlcude tests such as testing user creation, login, restrictions/authorizations, redirects, ride postings, feedback, and more.

## Other notes
The option to give feedback only shows up in the "my past rides" one calendar day after the ride time of the ride so testing that functionality is not possible in one sitting. The app stores media files in an AWS s3 bucket in order to avoid problems such as disappearing pictures caused by Heroku's ephemeral file system. The app uses the phone number inputed on the first login to send messages. This phone number can be updated in the profile page by scrolling down and selecting "change my phone number." If the phone number is not a valid US phone number, you will not receive text message notifications.
