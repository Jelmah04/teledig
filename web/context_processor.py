from .models import *

def user_notifications(request):
    if request.user.is_authenticated == True:
        notifications = UserNotification.objects.filter(user=request.user)
        notifications_count = UserNotification.objects.filter(user=request.user).exclude(read=True).count()

        return {
            'notifications': notifications,
            'notifications_count': notifications_count
        }
    else:
        notifications = UserNotification.objects.all()
        
        return {
            'notifications': notifications
        }
