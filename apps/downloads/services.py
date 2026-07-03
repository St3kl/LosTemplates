from .models import UserProductAccess


from .models import UserProductAccess


class DownloadService:

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
    def has_access(user, product):
        """
        Returns True if the user owns the product.
        """
        return UserProductAccess.objects.filter(
            user=user,
            product=product,
        ).exists()