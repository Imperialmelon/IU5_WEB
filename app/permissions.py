from rest_framework import permissions
from .redis import session_storage
from .models import User

class IsAuth(permissions.BasePermission):
    def has_permission(self, request, view):
        session_id = request.COOKIES['session_id']
        print(session_id)
        if session_id is None:
            return False
        try:
            session_storage.get(session_id).decode('utf-8')
        except:
            return False
        return True
    
class IsAuthManager(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        session_id = request.COOKIES['session_id']
        if session_id is None:
            return False
        try:
             user_name = session_storage.get(session_id).decode('utf-8')
        except:
            return False
        user = User.objects.filter(username=user_name).first()
        return user.is_staff