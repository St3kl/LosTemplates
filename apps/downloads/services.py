from .models import UserProductAccess


class DownloadService:
    """
    Handles ownership and download authorization.
    """

    @staticmethod
    def grant_access(user, product):
        """
        Grants permanent ownership of a product.
        """
        UserProductAccess.objects.get_or_create(
            user=user,
            product=product,
        )

    @staticmethod
    def revoke_access(user, product):
        """
        Removes ownership.
        """
        UserProductAccess.objects.filter(
            user=user,
            product=product,
        ).delete()

    @staticmethod
    def has_access(user, product):
        """
        Checks whether the user owns the product.
        """
        return UserProductAccess.objects.filter(
            user=user,
            product=product,
        ).exists()

    @staticmethod
    def owned_products(user):
        """
        Returns all products owned by the user.
        """
        return UserProductAccess.objects.filter(
            user=user
        ).select_related("product")