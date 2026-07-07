from .models import Wishlist


class WishlistService:

    @staticmethod
    def is_saved(user, product):

        return Wishlist.objects.filter(
            user=user,
            product=product,
        ).exists()

    @staticmethod
    def toggle(user, product):

        item = Wishlist.objects.filter(
            user=user,
            product=product,
        )

        if item.exists():
            item.delete()
            return False

        Wishlist.objects.create(
            user=user,
            product=product,
        )

        return True

    @staticmethod
    def user_items(user):

        return (
            Wishlist.objects
            .select_related("product")
            .filter(user=user)
        )