# from .models import Wishlist


# class WishlistService:
#     """
#     Business logic for the user's wishlist.
#     """

#     @staticmethod
#     def is_saved(user, product):
#         """
#         Return True if the product is already
#         in the user's wishlist.
#         """
#         return Wishlist.objects.filter(
#             user=user,
#             product=product,
#         ).exists()

#     @staticmethod
#     def toggle(user, product):
#         """
#         Add or remove a product from the wishlist.

#         Returns:
#             True  -> added
#             False -> removed
#         """

#         wishlist_item = Wishlist.objects.filter(
#             user=user,
#             product=product,
#         )

#         if wishlist_item.exists():
#             wishlist_item.delete()
#             return False

#         Wishlist.objects.create(
#             user=user,
#             product=product,
#         )

#         return True

#     @staticmethod
#     def user_items(user):
#         """
#         Return every wishlist item for the user.
#         """

#         return (
#             Wishlist.objects
#             .select_related(
#                 "product",
#                 "product__category",
#             )
#             .filter(user=user)
#             .order_by("-created_at")
#         )

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

    @staticmethod
    def count(user):
        """
        Return the number of wishlist items
        for the current user.
        """

        return Wishlist.objects.filter(
            user=user,
        ).count()