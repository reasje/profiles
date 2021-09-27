# include comes with a functionality of including 
# urls in the url patterns 
from django.urls import path , include
from django.views.generic import base
# from django.urls.conf import include 
# used to make a router
from rest_framework.routers import DefaultRouter

# importing api views
from profiles_api import views


router = DefaultRouter()
router.register('hello-viewset' , views.HelloViewSet , basename='hello-viewset')
# the reason that we do not give it a basename is that the queryset in the UserProfileViewSet
# handels the naming by accessing the model .
# you'll want to give the basename whenever you want to 
# set a the url without queryset or if you want to ovverride the name of 
# the query set that associated to it . 
router.register('profile' , views.UserProfileViewSet) 
router.register('feed' , views.UserProfileFeedViewSet)


urlpatterns=[
    # maping the api view to the url 
    path('hello-view/' , views.HelloApiView.as_view()),
    path('login/' , views.UserLoginApiView.as_view()),
    # the reason that we don't specify a fixed url is 
    # that we want to use the registred one 
    path('',include(router.urls))

]