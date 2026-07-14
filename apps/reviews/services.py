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
    
    
    @staticmethod
    def product_reviews(product):
        """
        Return all approved reviews
        for a product.
        """

        return (
            Review.objects
            .filter(
                product=product,
                approved=True,
            )
            .select_related("user")
            .order_by("-created_at")
        )


    @staticmethod
    def average_rating(product):
        """
        Calculate the average rating.
        """

        reviews = Review.objects.filter(
            product=product,
            approved=True,
        )

        if not reviews.exists():
            return 0

        total = sum(
            review.rating
            for review in reviews
        )

        return round(
            total / reviews.count(),
            1,
        )


    @staticmethod
    def total_reviews(product):
        """
        Total approved reviews.
        """

        return Review.objects.filter(
            product=product,
            approved=True,
        ).count()