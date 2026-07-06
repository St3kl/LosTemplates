from .models import Review

from apps.orders.models import OrderItem


class ReviewService:
    """
    Handles all review business logic.
    """

    @staticmethod
    def can_review(user, product):
        """
        User must have purchased the product.
        """

        return OrderItem.objects.filter(
            order__user=user,
            order__status="paid",
            product=product,
        ).exists()

    @staticmethod
    def has_review(user, product):
        """
        Prevent duplicate reviews.
        """

        return Review.objects.filter(
            user=user,
            product=product,
        ).exists()

    @staticmethod
    def create_review(
        *,
        user,
        product,
        rating,
        comment,
    ):
        """
        Create a review.
        """

        return Review.objects.create(
            user=user,
            product=product,
            rating=rating,
            comment=comment,
        )

    @staticmethod
    def update_review(
        review,
        *,
        rating,
        comment,
    ):
        """
        Update an existing review.
        """

        review.rating = rating
        review.comment = comment
        review.save()

        return review