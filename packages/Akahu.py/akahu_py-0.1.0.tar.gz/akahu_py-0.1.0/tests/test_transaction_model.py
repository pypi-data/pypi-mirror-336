from unittest import TestCase
from datetime import datetime

from akahu.models.transaction import Transaction
from akahu.utils import Utils


full_response = {
    "_id": "trans_cm7lcgcij010e08l4d8x80tnk",
    "_account": "acc_cm7h2wvtd000008jreiqeez7s",
    "_user": "user_cm5ncww0c003n08me2cng4fty",
    "_connection": "conn_cjgaaqcna000001ldwof8tvj0",
    "created_at": "2025-02-26T03:16:35.659Z",
    "updated_at": "2025-02-27T03:16:36.823Z",
    "date": "2025-02-26T02:23:40.000Z",
    "description": "COTTON ON MEGA 9936AUCKLAND CARD 0000",
    "amount": 15.99,
    "balance": 100.00,
    "type": "DEBIT",
    "hash": "acc_cm7h2wvtd000008jreiqeez7s-7e18ef971eba4d83423cf6de94539574",
    "meta": {
        "card_suffix": "0000",
        "logo": "https://cdn.akahu.nz/logos/merchants/merchant_cji9yur38000ganojm42oicsz",
    },
    "merchant": {
        "_id": "merchant_cji9yur38000ganojm42oicsz",
        "name": "Cotton On",
        "website": "https://cottonon.com/NZ/",
        "nzbn": "9429037893439",
    },
    "category": {
        "_id": "nzfcc_ckouvvydo001q08ml4xvgfhgl",
        "name": "Clothing stores",
        "groups": {
            "personal_finance": {
                "_id": "group_clasr0ysw0010hk4mf2dca4y8",
                "name": "Appearance",
            }
        },
    },
}

minimal_response = {
    "_id": "trans_cm7lcgcij010e08l4d8x80tnk",
    "_account": "acc_cm7h2wvtd000008jreiqeez7s",
    "_user": "user_cm5ncww0c003n08me2cng4fty",
    "_connection": "conn_cjgaaqcna000001ldwof8tvj0",
    "created_at": "2025-02-26T03:16:35.659Z",
    "updated_at": "2025-02-27T03:16:36.823Z",
    "date": "2025-02-26T02:23:40.000Z",
    "description": "COTTON ON MEGA 9936AUCKLAND CARD 0000",
    "amount": 15.99,
    "balance": 100.00,
    "type": "DEBIT",
    "hash": "acc_cm7h2wvtd000008jreiqeez7s-7e18ef971eba4d83423cf6de94539574",
    "meta": {},
}


class TestTransactionModel(TestCase):
    def setUp(self):
        self.full_transaction = Transaction(**full_response)
        self.minimal_transaction = Transaction(**minimal_response)

    def test_valid_full_transaction_parameters(self):
        transaction = self.full_transaction

        self.assertEqual(transaction.id, full_response["_id"])
        self.assertEqual(transaction.account, full_response["_account"])
        self.assertEqual(transaction.user, full_response["_user"])
        self.assertEqual(transaction.connection, full_response["_connection"])
        self.assertEqual(
            Utils.datetime_to_iso(transaction.created_at), full_response["created_at"]
        )
        self.assertEqual(
            Utils.datetime_to_iso(transaction.updated_at), full_response["updated_at"]
        )
        self.assertEqual(Utils.datetime_to_iso(transaction.date), full_response["date"])
        self.assertEqual(transaction.type, full_response["type"])
        self.assertEqual(transaction.amount, full_response["amount"])
        self.assertEqual(transaction.balance, full_response["balance"])
        self.assertDictEqual(transaction.meta, full_response["meta"])

    def test_valid_full_merchant_parameters(self):
        merchant = self.full_transaction.merchant
        merchant_response = full_response["merchant"]

        self.assertEqual(merchant.id, merchant_response["_id"])
        self.assertEqual(merchant.name, merchant_response["name"])
        self.assertEqual(merchant.website, merchant_response["website"])
        self.assertEqual(merchant.nzbn, merchant_response["nzbn"])

    def test_valid_full_category_parameters(self):
        category = self.full_transaction.category
        category_response = full_response["category"]

        self.assertEqual(category.id, category_response["_id"])
        self.assertEqual(category.name, category_response["name"])

    def test_valid_full_groups_parameters(self):
        groups = self.full_transaction.category.groups
        groups_response = full_response["category"]["groups"]
        groups_response["personal_finance_other"] = groups_response["personal_finance"]

        pass

    def test_valid_minimal_transaction_parameters(self):
        transaction = self.minimal_transaction

        self.assertEqual(transaction.id, minimal_response["_id"])
        self.assertEqual(transaction.account, minimal_response["_account"])
        self.assertEqual(transaction.user, minimal_response["_user"])
        self.assertEqual(transaction.connection, minimal_response["_connection"])
        self.assertEqual(
            Utils.datetime_to_iso(transaction.created_at),
            minimal_response["created_at"],
        )
        self.assertEqual(
            Utils.datetime_to_iso(transaction.updated_at),
            minimal_response["updated_at"],
        )
        self.assertEqual(
            Utils.datetime_to_iso(transaction.date), minimal_response["date"]
        )
        self.assertEqual(transaction.type, minimal_response["type"])
        self.assertEqual(transaction.amount, minimal_response["amount"])
        self.assertEqual(transaction.balance, minimal_response["balance"])
        self.assertDictEqual(transaction.meta, minimal_response["meta"])
        self.assertIsNone(transaction.merchant)
        self.assertIsNone(transaction.category)
