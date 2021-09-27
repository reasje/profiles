from django.contrib import admin

from profiles_api import models


admin.site.register(models.UserProfile)
# to register the profile feed item to the admin panel 
admin.site.register(models.ProfileFeedItem)
