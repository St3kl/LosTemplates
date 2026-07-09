from apps.analytics.models import (
    ProductView,
    ProductSale,
    ProductDownloadMetric,
)


class AnalyticsService:


    @staticmethod
    def track_product_view(
        product,
        user=None,
        ip_address=None,
    ):
        """
        Records a product page visit.
        """

        ProductView.objects.create(
            product=product,
            user=user,
            ip_address=ip_address,
        )



    @staticmethod
    def track_sale(
        product,
        user,
        price,
    ):
        """
        Records completed purchase.
        """

        ProductSale.objects.create(
            product=product,
            user=user,
            price=price,
        )



    @staticmethod
    def track_download(
        product,
        user,
    ):
        """
        Records successful download.
        """

        ProductDownloadMetric.objects.create(
            product=product,
            user=user,
        )