from rest_framework import permissions


class UpdateOwnProfile(permissions.BasePermission):
    """Allow user to edit their own proifile"""

    def has_object_permission(self, request , view , obj):
        """Check user is trying to edit their own profile"""
        # first we need to check the http method that is being called is a 
        # safe method or not , the safe method is get method .
        if request.method in permissions.SAFE_METHODS:
            # returning true means the operation  does not have problem and can be made
            return True
        
        # if it is not a safe method we want to see the user is trying 
        # not the safe method is their own id or not .
        return obj.id == request.user.id


class UpdateOwnStatus(permissions.BasePermission):
    """Allow users to update their own status"""

    def has_object_permission(self, request, view, obj):
        """Check the user is trying to update their own status"""
        if request.method in permissions.SAFE_METHODS:
            return True
            
        return obj.user_profile.id == request.user.id 

