from .models import OrderItem


def user_can_access_item(user, item_id):

    return OrderItem.objects.filter(
        id=item_id,
        order__user=user,
        order__status="paid"
    ).exists()