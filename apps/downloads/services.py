from .models import UserProductAccess


class DownloadService:

    @staticmethod
    def grant_access(user, product):
        """
        Grants permanent access to a purchased product.
        """

        UserProductAccess.objects.get_or_create(
            user=user,
            product=product,
        )