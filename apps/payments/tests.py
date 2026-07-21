from decimal import Decimal
from unittest.mock import patch

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from apps.downloads.models import UserProductAccess
from apps.orders.models import Order, OrderItem
from apps.products.models import Category, Product

from .models import Payment
from .services import PaystackService

import hashlib
import hmac
import json

from django.conf import settings
from django.test import TestCase

from apps.payments.webhooks import process_webhook

class PaymentCompletionTests(TestCase):


    def setUp(self):

        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="password123",
        )

        self.category = Category.objects.create(
            name="Test Category",
            slug="test-category",
        )

        self.product = Product.objects.create(
            category=self.category,
            title="Test Product",
            slug="test-product",
            short_description="Test product",
            description="Test product description",
            price=Decimal("29.00"),
            active=True,
        )

        self.order = Order.objects.create(
            user=self.user,
            status="pending",
            total_price=Decimal("29.00"),
        )

        self.item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=Decimal("29.00"),
        )

        self.payment = Payment.objects.create(
            user=self.user,
            order=self.order,
            reference="test-reference-123",
            amount=Decimal("29.00"),
            status="pending",
        )

        self.gateway_response = {
            "status": True,
            "data": {
            "id": 123456,
            "reference": "test-reference-123",
            "status": "success",
        },
    }

    def test_payment_completion_marks_payment_successful(self):

        result = PaystackService.complete_payment(
            payment=self.payment,
            gateway_response=self.gateway_response,
        )

        self.assertEqual(
            result["status"],
            "success",
        )

        self.payment.refresh_from_db()

        self.assertEqual(
            self.payment.status,
            "success",
        )

    def test_payment_completion_marks_order_paid(self):

        PaystackService.complete_payment(
            payment=self.payment,
            gateway_response=self.gateway_response,
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.status,
            "paid",
        )

    def test_payment_grants_product_access(self):

        PaystackService.complete_payment(
            payment=self.payment,
            gateway_response=self.gateway_response,
        )

        self.assertTrue(
            UserProductAccess.objects.filter(
                user=self.user,
                product=self.product,
            ).exists()
        )

    def test_duplicate_payment_is_not_processed_twice(self):

        first_result = PaystackService.complete_payment(
            payment=self.payment,
            gateway_response=self.gateway_response,
        )

        second_result = PaystackService.complete_payment(
            payment=self.payment,
            gateway_response=self.gateway_response,
        )

        self.assertEqual(
            first_result["status"],
            "success",
        )

        self.assertEqual(
            second_result["status"],
            "already_processed",
        )


class PaymentCallbackTests(TestCase):


    def setUp(self):

        self.user = User.objects.create_user(
            username="callbackuser",
            email="callback@example.com",
            password="password123",
        )

        self.category = Category.objects.create(
            name="Callback Category",
            slug="callback-category",
        )

        self.product = Product.objects.create(
            category=self.category,
            title="Callback Product",
            slug="callback-product",
            short_description="Callback product",
            description="Callback product description",
            price=Decimal("29.00"),
            active=True,
        )

        self.order = Order.objects.create(
            user=self.user,
            status="pending",
            total_price=Decimal("29.00"),
        )

        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=Decimal("29.00"),
        )

        self.payment = Payment.objects.create(
            user=self.user,
            order=self.order,
            reference="callback-reference",
            amount=Decimal("29.00"),
            status="pending",
        )

        self.client.login(
            username="callbackuser",
            password="password123",
        )

    @patch(
        "apps.payments.views.PaystackService.verify_payment"
    )
    def test_successful_callback(
        self,
        mock_verify_payment,
    ):

        mock_verify_payment.return_value = {
            "status": True,
            "data": {
                "id": 123456,
                "reference": "callback-reference",
                "status": "success",
                "amount": 2900,
                "customer": {
                "email": "callback@example.com",
                },
            },
        }

        response = self.client.get(
            reverse(
                "payments:callback",
            ),
            {
                "reference": "callback-reference",
            },
        )

        self.assertRedirects(
            response,
            reverse(
                "accounts:downloads",
            ),
        )

        self.payment.refresh_from_db()

        self.assertEqual(
            self.payment.status,
            "success",
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.status,
            "paid",
        )

    @patch(
        "apps.payments.views.PaystackService.verify_payment"
    )
    def test_callback_rejects_wrong_amount(
    self,
    mock_verify_payment,
):

        mock_verify_payment.return_value = {
            "status": True,
            "data": {
                "id": 123456,
                "reference": "callback-reference",
                "status": "success",
                "amount": 9999,
                "customer": {
                "email": "callback@example.com",
                },
            },
        }

        response = self.client.get(
            reverse(
                "payments:callback",
            ),
            {
                "reference": "callback-reference",
            },
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.payment.refresh_from_db()

        self.assertEqual(
            self.payment.status,
            "pending",
        )

    @patch(
        "apps.payments.views.PaystackService.verify_payment"
    )
    def test_callback_rejects_wrong_customer(
        self,
        mock_verify_payment,
    ):

        mock_verify_payment.return_value = {
            "status": True,
            "data": {
                "id": 123456,
                "reference": "callback-reference",
                "status": "success",
                "amount": 2900,
                "customer": {
                "email": "attacker@example.com",
                },
            },
        }

        response = self.client.get(
            reverse(
                "payments:callback",
            ),
            {
                "reference": "callback-reference",
            },
        )

        self.assertEqual(
            response.status_code,
            400,
        )

        self.payment.refresh_from_db()

        self.assertEqual(
            self.payment.status,
            "pending",
        )
        
class PaymentWebhookTests(TestCase):

    def setUp(self):

        self.user = User.objects.create_user(
            username="webhookuser",
            email="webhook@example.com",
            password="password123",
        )

        self.category = Category.objects.create(
            name="Webhook Category",
            slug="webhook-category",
        )

        self.product = Product.objects.create(
            category=self.category,
            title="Webhook Product",
            slug="webhook-product",
            short_description="Webhook product",
            description="Webhook product description",
            price=Decimal("29.00"),
            active=True,
        )

        self.order = Order.objects.create(
            user=self.user,
            status="pending",
            total_price=Decimal("29.00"),
        )

        OrderItem.objects.create(
            order=self.order,
            product=self.product,
            price=Decimal("29.00"),
        )

        self.payment = Payment.objects.create(
            user=self.user,
            order=self.order,
            reference="webhook-reference",
            amount=Decimal("29.00"),
            status="pending",
        )

        self.payload = {
            "event": "charge.success",
            "data": {
                "id": 987654,
                "reference": "webhook-reference",
                "status": "success",
            },
        }

    def generate_signature(self, payload):

        body = json.dumps(
            payload,
        ).encode()

        return hmac.new(
            settings.PAYSTACK_SECRET_KEY.encode(),
            body,
            hashlib.sha512,
        ).hexdigest()

    def test_successful_webhook_processes_payment(self):

        body = json.dumps(
            self.payload,
        )

        signature = self.generate_signature(
            self.payload,
        )

        response = self.client.post(
            "/payments/webhook/",
            data=body,
            content_type="application/json",
            HTTP_X_PAYSTACK_SIGNATURE=signature,
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.payment.refresh_from_db()

        self.assertEqual(
            self.payment.status,
            "success",
        )

        self.order.refresh_from_db()

        self.assertEqual(
            self.order.status,
            "paid",
        )

    def test_webhook_rejects_invalid_signature(self):

        body = json.dumps(
            self.payload,
        )

        response = self.client.post(
            "/payments/webhook/",
            data=body,
            content_type="application/json",
            HTTP_X_PAYSTACK_SIGNATURE="invalid-signature",
        )

        self.assertEqual(
            response.status_code,
            403,
        )

        self.payment.refresh_from_db()

        self.assertEqual(
            self.payment.status,
            "pending",
        )

    def test_webhook_rejects_missing_signature(self):

        body = json.dumps(
            self.payload,
        )

        response = self.client.post(
            "/payments/webhook/",
            data=body,
            content_type="application/json",
        )

        self.assertEqual(
            response.status_code,
            403,
        )

    def test_webhook_rejects_invalid_json(self):

        signature = hmac.new(
            settings.PAYSTACK_SECRET_KEY.encode(),
            b"invalid-json",
            hashlib.sha512,
        ).hexdigest()

        response = self.client.post(
            "/payments/webhook/",
            data="invalid-json",
            content_type="application/json",
            HTTP_X_PAYSTACK_SIGNATURE=signature,
        )

        self.assertEqual(
            response.status_code,
            400,
        )

    def test_webhook_ignores_unknown_event(self):

        payload = {
            "event": "unknown.event",
            "data": {},
        }

        body = json.dumps(
            payload,
        )

        signature = self.generate_signature(
            payload,
        )

        response = self.client.post(
            "/payments/webhook/",
            data=body,
            content_type="application/json",
            HTTP_X_PAYSTACK_SIGNATURE=signature,
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.payment.refresh_from_db()

        self.assertEqual(
            self.payment.status,
            "pending",
        )

    def test_webhook_handles_unknown_payment_reference(self):

        payload = {
            "event": "charge.success",
            "data": {
                "reference": "does-not-exist",
            },
        }

        body = json.dumps(
            payload,
        )

        signature = self.generate_signature(
            payload,
        )

        response = self.client.post(
            "/payments/webhook/",
            data=body,
            content_type="application/json",
            HTTP_X_PAYSTACK_SIGNATURE=signature,
        )

        self.assertEqual(
            response.status_code,
            200,
        )

        self.payment.refresh_from_db()

        self.assertEqual(
            self.payment.status,
            "pending",
        )

