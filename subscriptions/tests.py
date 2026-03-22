from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Subscription, PlanTier

User = get_user_model()


class SubscriptionTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='subuser', password='password123')
        self.tier = PlanTier.objects.create(
            name="Pro", price=19.99, stripe_price_id="abc")
        self.sub = Subscription.objects.create(
            user=self.user, plan_tier=self.tier, status='incomplete')

    def test_is_premium_property(self):
        """Tests the is_premium helper on the model"""
        self.assertFalse(self.sub.is_premium)
        self.sub.status = 'active'
        self.sub.save()
        self.assertTrue(self.sub.is_premium)


class MonetizationTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='customer', password='password123')
        self.tier = PlanTier.objects.create(
            name="Pro", price=19.99, stripe_price_id="price_123")

    def test_default_subscription_status(self):
        """Verify users start as incomplete/free"""
        sub = Subscription.objects.create(user=self.user, plan_tier=self.tier)
        self.assertEqual(sub.status, 'incomplete')
        self.assertFalse(sub.is_premium)

    def test_active_subscription_access(self):
        """Verify is_premium property turns True when active"""
        sub = Subscription.objects.create(
            user=self.user, plan_tier=self.tier, status='active')
        self.assertTrue(sub.is_premium)

    def test_plan_tier_string_representation(self):
        """Ensures Euro formatting in admin/models is working"""
        self.assertIn("€19.99", str(self.tier))
