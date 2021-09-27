# hold all  the models of the app in here 
from django.db import models
# default libs when creating a model 
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
# this import is for the UserProfileManager
from django.contrib.auth.models import BaseUserManager
# this class to tell how to interact with the UserProfiles that werer created
# this fun interacts with the django createsuperuser fun  
# this import is to access authentication 
from django.conf import settings

class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    # for all class funs we add self as the parameter 
    # create_user is a fun assigned with django createsuperuser
    # password=None is a argument if not given it will be set to None
    # because of the django password checking system works none 
    # password will not be working 
    def create_user(self , email , name , password=None):
        """Create a new suer profile"""
        # if the email was passed as a null string 
        # this will try to throw a exception 
        # this is how the standard django 
        # error handeling works 
        if not email:
            raise ValueError('User must have an email address')
        
        # the email some times are given with uppercases 
        # because all the email providers are not 
        # case sensetive we will reformat the email
        # as the common format for the email 
        email = self.normalize_email(email)
        user = self.model(email=email , name=name)

        # we cannot pass the password via argument 
        # this way the password gets hashed 
        user.set_password(password)
        # fun below tells the django that 
        # every database that you use 
        # will be saved on that 
        user.save(using=self.db)
        return user

    def create_superuser(self , email , name , password):
        """Create and save a new superuser with given details"""
        # getting the user form the create_user fun 
        user = self.create_user(email , name , password)

        # making the properties True
        user.is_superuser = True
        user.is_staff = True
        # django default model saver 
        user.save(using=self._db)

        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    # This is a dock String
    """Database model for users in the system"""
    # defining the fields 

    # having the max length
    # every email must be unique 
    email = models.EmailField(max_length=255 , unique=True)
    name = models.CharField(max_length=255)
    # by default when the a UserProfile is created is_active will be set to True
    is_activate =models.BooleanField(default=True)
    # by default when the a UserProfile is created is_staff will be set to False
    is_staff = models.BooleanField(default=False)

    # models manager is a tool to tell django 
    # how to create UserProfile 
    # how to delete UserProfile
    # and so on ...
    objects = UserProfileManager()

    # again for working with django admin 
    # we must include these two fields
    # by default the USERNAME_FIELD is the email field
    # and by default the USERNAME_FIELD is required 
    # and when linking this to the email field 
    # the email field will be required too  
    USERNAME_FIELD = 'email'
    # this is how to add other required fields
    # with the code above the name field will be required 
    REQUIRED_FIELDS = ['name']

    # this fun will return the full name of object 
    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    # this fun will return the short name of object 
    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    # this fun will return the string type of the object 
    def __str__(self):
        """Return String representation of our user"""
        return self.email


class ProfileFeedItem(models.Model):
    """Profile status update"""
    # linking a model to other models in django 
    # is foreign key . 
    # this allows you to know the integrity (being correct) of the 
    # database , for example you cannot create a profile feed item without 
    # having a profile .
    user_profile = models.ForeignKey(
        # we can give it UserProfile but it't like being hard coded
        # and once you change the user model you have to change them by hand .
        settings.AUTH_USER_MODEL,
        # on delete tells the django when the linked model has 
        # been deleted and it deletes this model too .
        # CASCADE : cascades the changes down to other models
        # null : would set the value of the user_profile to null but here we want to 
        # delete the feed item to that User Profile .
        on_delete=models.CASCADE
    )
    status_text = models.CharField(max_length=255)
    # manualy set the time when created 
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """Return the model as a string"""
        return self.status_text