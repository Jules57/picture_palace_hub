from decimal import Decimal

from django.test import TestCase
from users.models import Customer


class CustomerModelTest(TestCase):

    def setUp(self):
        self.customer = Customer.objects.create(username='testuser')

    def test_customer_creation(self):
        # assertIsInstance
        self.assertTrue(isinstance(self.customer, Customer))
        self.assertEqual(str(self.customer), self.customer.username)

    def test_customer_default_balance(self):
        new_customer = Customer.objects.create(
                username='newuser',
                password='newpassword'
        )
        self.assertEqual(new_customer.balance, Decimal('10000000.00'))
