from django.utils import timezone

from .models import Coupon


class CouponService:


    @staticmethod
    def validate(code):
        """
        Validate coupon availability.
        """

        try:
            coupon = Coupon.objects.get(
                code__iexact=code
            )

        except Coupon.DoesNotExist:
            return None


        now = timezone.now()


        if not coupon.active:
            return None


        if coupon.times_used >= coupon.usage_limit:
            return None


        if now < coupon.valid_from:
            return None


        if now > coupon.valid_until:
            return None


        return coupon



    @staticmethod
    def calculate_discount(
        coupon,
        amount,
    ):
        """
        Calculate discount amount.
        """


        if coupon.discount_type == "percentage":

            discount = (
                amount
                *
                coupon.value
                /
                100
            )


        elif coupon.discount_type == "fixed":

            discount = coupon.value


        else:

            discount = 0



        # Never allow discount bigger than price

        if discount > amount:
            discount = amount


        return discount