# This imports are for making the api to it's standard form 
from rest_framework.serializers import Serializer
from rest_framework.views import APIView 
from rest_framework.response import Response
# status is a handy status codes for returning responses 
from rest_framework import status
from rest_framework import viewsets
# generates a random token when the user logs in 
# authenthicate the user by that token 
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
# below import is used to make authantication token 
from rest_framework.authtoken.views import ObtainAuthToken
# used in renderer_classes in the UserLoginApiView
from rest_framework.settings import api_settings
# the view set is read only if the user is not authenticated 
# from rest_framework.permissions import IsAuthenticatedOrReadOnly
# the below imnport blocks even viewing feeds for not authenticated users
from rest_framework.permissions import IsAuthenticated

# our serializer 
from profiles_api import serializers
# importing the needed model  
from profiles_api import models
from profiles_api import permissions


class HelloApiView(APIView):
    """Test API View"""
    # adding serializer to the api 
    serializer_class = serializers.HelloSerializers

    # used when retrieving an object or list of objects 
    # we are going to give the HelloApiView a url 
    # so when the request is with get method this fun will be callled 
    # parameters : self is for all class funs ,
    # request is request object provided with rest_framework
    # and takes whatever was on the request with itself 
    # to the method ,
    # format is a argument which is used to add the format 
    # suffix to the endpoint 
    def get(self,request , format=None):
        """Returns a list of APIView features"""

        an_apiview = [
            'Uses HTTP methods as function (get , post , patch , put , delete)',
            'Is similar to a traditional Django View',
            'Gives you the most control over you application logic ',
            'Is mapped manually to URLs',
        ]

        return Response({'message' : 'Hello!' , 'an_apiview' : an_apiview})

    def post(self , request):
        """Create a hello message with our name"""
        # self.serializer is fun that comes with Api view 
        # when a post request has been made the data will 
        # be passed throw request 
        serializer = self.serializer_class(data=request.data)


        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}'
            return Response({'message' : message})
        else:
            return Response(serializer.errors ,status=status.HTTP_400_BAD_REQUEST )

    # pk  is the id primary key or the id of the object 
    # to be updated 
    # put replaces an object not updating a single field 
    # if you had name and lastname and again the name was send with 
    # put method then the lastname whatever was became a null value 
    # cause it has not been provided 
    def put(self , request , pk=None):
        """Handle updating an object"""
        return Response({'method' : 'PUT'})

    def patch(self, request , pk=None):
        """Handle partial update of an object"""
        return Response({'method': 'patch'})

    def delete(self , request , pk=None):
        """Delete an object"""
        return Response({'method': "delete"})


# Why to use view sets : 
# 1. A simple CRUD interface to your database 
# 2. A quick and simple API 
# 3. Little to no customization on the logic 
# 4. Woking with standard data structures 
class HelloViewSet(viewsets.ViewSet):
    """Test API ViewSet"""
    # adding serializer to the api 
    serializer_class = serializers.HelloSerializers

    # like a get
    def list(self , request):
        """Rreturn a hello message"""
        a_viewset = [
            'Uses HTTP methods as function (list , create , retrieve , partial_update , delete)',
            'Automatically maps to URLs using Routers',
            'Provides more funcionality with less code',
        ]        

        return Response({'message' : 'Hello' , 'a_viewset' : a_viewset})

    def create(self , request):
        """Create a new hello message"""
        serializer = self.serializer_class(data=request.data)
    
        if serializer.is_valid():
            name = serializer.validated_data.get('name')
            message = f'Hello {name}!'
            return Response({'message' : message})
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
    
    def retrieve(self , request , pk=None):
        """Handle getting an object by it's ID"""
        return Response({'http_methid' : 'GET'})

    def update(self , request , pk=None):
        """Handle updating an object"""
        return Response({'http_method': 'PUT'})

    def partial_update(self , request , pk=None):
        """Handle updating part of an object"""
        return Response({'http_method': 'PATCH'})

    def destroy(self, request , pk=None):
        """Handle removing an object """
        return Response({'http_method' : 'DELETE'})

# making profile api 

# creating new profile
    # Handle registration of new users 
    # Validate profile data

# listing existing profiles
    # Search for profiles
    # Email and name 

# view specific profiles 
    # profile ID

# update profile of logged in user 
    # change name , email , and password 

# delete profile 

# /api/profile/ --> GET list all profiles 
# /api/profile/ --> POST create a new profile 

# /api/profile/<profile_id>/ --> GET view a specific profile 
#                            --> PUT / PATCH update a profile
#                            --> DELETE remove it completely using


class UserProfileViewSet(viewsets.ModelViewSet):
    """Handle creating and updating profiles"""
    serializer_class = serializers.UserProfileSerializer
    # django is aware of the standard operations you'll 
    # need to perform on the objects
    queryset = models.UserProfile.objects.all()
    # we use the " , " to make it tuple  
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.UpdateOwnProfile,)
    # adding the search option to the api 
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name' , 'email',)


class UserLoginApiView(ObtainAuthToken):
    """Handle creating user authentication tokens"""
    renderer_classes= api_settings.DEFAULT_RENDERER_CLASSES


# making feed api 
# api/feed/ --> list all feed items 
#            --> GET (list feed items)
#            --> POST (create feed item for logged in user)
# api/feed/<feed_item_id>/ --> manage specific feed items
#                          --> GET (get the feed item)
#                          --> PUT/ PATCH  (update feed item)
#                          --> DELETE (delete item)

class UserProfileFeedViewSet(viewsets.ModelViewSet):
    """Handles creating , reading and updating profile feed items"""
    authentication_classes = (TokenAuthentication,)
    serializer_class = serializers.ProfileFeeditemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (
        permissions.UpdateOwnStatus,
        # lets prevent creating feed item when they are not authenticated 
        # in profile api if you were not authenticated you could make 
        # user_profile but in feed you can not make a feed item , 
        # if you are not authenticated .
        IsAuthenticated
    )
    # when the new object has been created django calls 
    # the fun below and passes the serializer
    def perform_create(self , serializer):
        """Sets the user profile to the logged in user"""
        # and while creating the new object that has been validated
        # we pass the user profile that is making the request to make the 
        # feed item and because we have added authentication ,
        # the user can perform this action if he has been authenticated .
        serializer.save(user_profile=self.request.user)
