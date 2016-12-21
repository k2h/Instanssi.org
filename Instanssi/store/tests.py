# -*- coding: utf-8 -*-

import uuid

from Instanssi.store.models import TransactionItem
from Instanssi.store.handlers import begin_payment_process, validate_item, TransactionException
from Instanssi.common.testing.store import StoreTestData, BitpayFakeResponse, PaytrailFakeResponse
from Instanssi.common.testing.kompomaatti import KompomaattiTestData
from Instanssi.common.testing.utils import q_reverse

from django.test import TestCase
from django.core.urlresolvers import reverse
import mock


class StoreTests(TestCase):
    def setUp(self):
        self.event = KompomaattiTestData.create_test_event('TestEvent')
        self.items = []
        self.variants = {}
        for i in range(5):
            item = StoreTestData.create_test_item("TestItem {}".format(i), self.event, sort_index=i)
            self.items.append(item)
            self.variants[i] = StoreTestData.create_test_variants(item, 5)

        # Item 4 is not available
        self.items[4].available = False
        self.items[4].save()

        # Item 3 max product count is 0 (should not be available)
        self.items[3].max = 0
        self.items[3].save()

        # Item 2 has a discount with 5 items by 50%
        self.items[2].discount_amount = 5
        self.items[2].discount_percentage = 50
        self.items[2].save()

        # Create a test transaction
        self.transaction = StoreTestData.create_test_transaction(self.items, self.variants)

    def test_validate_item(self):
        """ Make sure that item validation function works """
        item_tpl = {
            "item_id": self.items[0].id,
            "variant_id": None,
            "amount": 1
        }

        # Make sure too large or zero amount fails, but small enough does not
        validate_item({**item_tpl, **{"amount": 5}})
        with self.assertRaises(TransactionException):
            self.assertRaises(validate_item({**item_tpl, **{"amount": 6}}), TransactionException)
            self.assertRaises(validate_item({**item_tpl, **{"amount": 0}}), TransactionException)

        # Make sure item id checking works
        validate_item({**item_tpl, **{"item_id": self.items[0].id}})
        with self.assertRaises(TransactionException):
            validate_item({**item_tpl, **{"item_id": self.items[4].id}})  # available is False
            validate_item({**item_tpl, **{"item_id": self.items[3].id}})  # Max is 0

        # Make sure variant id checking works
        validate_item({**item_tpl, **{"item_id": self.items[1].id, "variant_id": self.variants[1][0].id}})
        validate_item({**item_tpl, **{"item_id": self.items[1].id, "variant_id": self.variants[1][4].id}})
        with self.assertRaises(TransactionException):
            # Fail if variant does not belong to the product
            validate_item({**item_tpl, **{"item_id": self.items[1].id, "variant_id": self.variants[2][0].id}})

    def test_create_transaction(self):
        """ Make sure transaction creation works as it should, and make sure that values look as they should """
        ta = self.transaction

        # Make sure the data fields have been filled
        self.assertEqual(len(ta.key), 32)
        self.assertNotEqual(ta.time_created, None)
        self.assertEqual(ta.firstname, "Donald")
        self.assertEqual(ta.lastname, "Duck")
        self.assertEqual(ta.company, "None")
        self.assertEqual(ta.email, "donald.duck@duckburg.inv")
        self.assertEqual(ta.telephone, "991234567")
        self.assertEqual(ta.mobile, "+358991234567")
        self.assertEqual(ta.street, "1313 Webfoot Walk")
        self.assertEqual(ta.postalcode, "00000")
        self.assertEqual(ta.city, "Duckburg")
        self.assertEqual(ta.country, "US")
        self.assertEqual(ta.information, "Quack, damn you!")
        self.assertEqual(ta.token, '')
        self.assertEqual(ta.time_pending, None)
        self.assertEqual(ta.time_cancelled, None)
        self.assertEqual(ta.time_paid, None)
        self.assertEqual(ta.payment_method_name, '')

        # Test properties
        self.assertEqual(ta.is_cancelled, False)
        self.assertEqual(ta.is_delivered, False)
        self.assertEqual(ta.is_pending, False)
        self.assertEqual(ta.is_paid, False)
        self.assertEqual(ta.full_name, "Donald Duck")

        # Make sure this doesn't crash
        self.assertEqual(ta.qr_code.startswith("http"), True)

        # Check price functions
        self.assertEqual(ta.get_transaction_items().count(), 6)
        self.assertEqual(ta.get_total_price(), 70)  # Note discounts
        self.assertEqual(ta.get_storeitem_count(self.items[0]), 1)
        self.assertEqual(ta.get_storeitem_count(self.items[2]), 5)
        self.assertEqual(ta.get_storeitem_count(self.items[1]), 0)

        # Make sure transaction items went through
        for item in ta.get_transaction_items():
            self.assertIn(item.item.id, [self.items[0].id, self.items[2].id])
            self.assertNotEqual(item.variant, None)
            self.assertEqual(item.time_delivered, None)
            self.assertEqual(len(item.key), 32)
            self.assertEqual(item.is_delivered, False)
            self.assertEqual(item.qr_code.startswith("http"), True)

        # Check amounts (manually)
        self.assertEqual(TransactionItem.objects.filter(transaction=ta, item=self.items[0]).count(), 1)
        self.assertEqual(TransactionItem.objects.filter(transaction=ta, item=self.items[2]).count(), 5)

        # Check discount(s)
        discount_items = TransactionItem.objects.filter(transaction=ta, item=self.items[2])
        for item in discount_items:
            self.assertEqual(item.original_price, 20)
            self.assertEqual(item.purchase_price, 10)
        non_discount_item = TransactionItem.objects.get(transaction=ta, item=self.items[0])
        self.assertEqual(non_discount_item.original_price, 20)
        self.assertEqual(non_discount_item.purchase_price, 20)

    @mock.patch('Instanssi.store.utils.paytrail.requests.post',
                return_value=PaytrailFakeResponse(401, PaytrailFakeResponse.create_failure()))
    def test_paytrail_begin_payment_process_bad_request(self, mock_post):
        """ Make sure paytrail fails properly (we should get a failure redirect url) """
        result = begin_payment_process(1, self.transaction)
        self.assertEqual(result, reverse('store:pm:paytrail-failure'))
        self.assertEqual(self.transaction.token, '')

    @mock.patch('Instanssi.store.utils.paytrail.requests.post',
                return_value=PaytrailFakeResponse(201, PaytrailFakeResponse.create_success(order_no="234246654",
                                                                             token=uuid.uuid4().hex)))
    def test_paytrail_begin_payment_process_good_request(self, mock_post):
        """ Make sure paytrail works with a good request (we should get a redirect URL) """
        result = begin_payment_process(1, self.transaction)
        self.transaction.refresh_from_db()
        self.assertNotEqual(self.transaction.token, None)
        self.assertEqual(self.transaction.payment_method_name, "Paytrail")
        self.assertEqual(result, "https://payment.paytrail.com/payment/load/token/{}".format(self.transaction.token))

    @mock.patch('Instanssi.store.utils.bitpay.requests.post',
                return_value=BitpayFakeResponse(401, BitpayFakeResponse.create_failure()))
    def test_bitpay_begin_payment_process_bad_request(self, mock_post):
        """ Make sure bitpay fails properly (we should get a failure redirect url) """
        result = begin_payment_process(0, self.transaction)
        self.assertEqual(result, reverse('store:pm:bitpay-failure'))

    @mock.patch('Instanssi.store.utils.bitpay.requests.post',
                return_value=BitpayFakeResponse(201, BitpayFakeResponse.create_success(order_no="3456454560")))
    def test_bitpay_begin_payment_process_good_request(self, mock_post):
        """ Make sure bitpay works with a good request (we should get a redirect URL) """
        result = begin_payment_process(0, self.transaction)
        self.transaction.refresh_from_db()
        self.assertEqual(self.transaction.token, '3456454560')
        self.assertEqual(self.transaction.payment_method_name, "Bitpay")
        self.assertEqual(result, "https://test.bitpay.com/invoice?id={}".format(self.transaction.token))

    def test_paytrail_success_endpoint(self):
        # TODO: Implement this
        ta = StoreTestData.create_full_started_transaction()
        url = q_reverse('store:pm:paytrail-success', query={
            'ORDER_NUMBER': ta.id,
            'TIMESTAMP': 0,
            'PAID': 'asd',
            'METHOD': 2,
            'RETURN_AUTHCODE': ''
        })
        result = self.client.get(url)
        self.assertTemplateUsed(result, 'store/success.html')
        self.assertEqual(result.status_code, 200)

    def test_paytrail_notify_endpoint(self):
        # TODO: Implement this
        #result = self.client.get(reverse('store:pm:paytrail-notify'))
        #self.assertEqual(result.status_code, 200)
        pass

    def test_paytrail_failure_endpoint(self):
        """
        Test paytrail failure endpoint. Note that this should be only a static page, no other functionality.
        """
        result = self.client.get(reverse('store:pm:paytrail-failure'))
        self.assertTemplateUsed(result, 'store/failure.html')
        self.assertEqual(result.status_code, 200)

    def test_bitpay_success_endpoint(self):
        """
        Test bitpay success endpoint. Note that this should be only a static page, no other functionality.
        """
        result = self.client.get(reverse('store:pm:bitpay-success'))
        self.assertTemplateUsed(result, 'store/success.html')
        self.assertEqual(result.status_code, 200)

    def test_bitpay_notify_endpoint(self):
        # TODO: Implement this
        #result = self.client.get(reverse('store:pm:bitpay-notify'))
        #self.assertEqual(result.status_code, 200)
        pass

    def test_bitpay_failure_endpoint(self):
        """
        Test bitpay failure endpoint. Note that this should be only a static page, no other functionality.
        """
        result = self.client.get(reverse('store:pm:bitpay-failure'))
        self.assertTemplateUsed(result, 'store/failure.html')
        self.assertEqual(result.status_code, 200)
