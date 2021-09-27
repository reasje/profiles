# a serializer helps you to convert data inputs to python 
# objects vs , like when your getting input from a post method .
from django.contrib.auth.models import User
from rest_framework import serializers

from profiles_api import models


class HelloSerializers(serializers.Serializer):
    """Serializes a name field for testing our APIView"""
    # specify a class 
    # specity fields 
    name = serializers.CharField(max_length = 10)

class UserProfileSerializer(serializers.ModelSerializer):
    """Serializes a user profile object"""

    # Meta class is used to configure a serializer 
    # to the point to get to a model 
    class Meta:
        # this sets the user profile to point to our UserPorfileSerializer 
        model = models.UserProfile
        # these are the fields to make our models according to them 
        fields = ('id' , 'email' , 'name' , 'password')
        # we want to set up some rules upon the password 
        # and make it write_only to prevent future changes 
        extra_kwargs = {
            'password' : {
                # prevents retrieve operation 
                'write_only' : True,
                'style' : {'input_type' : 'password'}
            }
        }

    # the reason to ovverride the create fun is to have 
    # the ability to hash our password   
    def create(self , validated_data):
        """Create and return a new user"""
        # ovveriding the create_user fun pre defined in the 
        # UserProfileManager but the objects property gives access to the 
        # user profile manager
        user = models.UserProfile.objects.create_user(
            email=validated_data['email'],
            name=validated_data['name'],
            password=validated_data['password']
        )

        return user


class ProfileFeeditemSerializer(serializers.ModelSerializer):
    """Serializes a profile feed items"""

    class Meta:
        model= models.ProfileFeedItem
        # always the id is read only 
        # the created is read only too  
        # only fields that will be writable are 
        # status_text , user_profile  
        # we want to set the user profile to be the one that is authonticated 
        # and also unchangable .
        fields = ('id' , 'user_profile' , 'status_text' , 'created_on')
        extra_kwargs = {
            'user_profile' : {'read_only' : True}
        }



