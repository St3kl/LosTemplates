from .models import Notification


def notifications_context(request):
    """
    Adds notification data globally to every template.
    """

    if not request.user.is_authenticated:

        return {
            "unread_notifications_count": 0,
        }

    unread_count = Notification.objects.filter(
        user=request.user,
        is_read=False,
    ).count()

    return {
        "unread_notifications_count": unread_count,
    }
    
    
def unread_notifications(request):

    if not request.user.is_authenticated:

        return {
            "unread_notifications_count": 0,
        }

    unread_count = Notification.objects.filter(
        user=request.user,
        is_read=False,
    ).count()

    return {
        "unread_notifications_count": unread_count,
    }