from unittest import TestCase

from akahu.models.account import Account
from akahu.utils import Utils

response = {
    "_id": "acc_id",
    "_credentials": "creds_credentials",
    "connection": {
        "name": "ASB",
        "logo": "https://cdn.akahu.nz/logos/connections/conn_cjgaaqcna000001ldwof8tvj0",
        "_id": "conn_cjgaaqcna000001ldwof8tvj0",
    },
    "name": "Checking",
    "formatted_account": "12-3072-0057595-51",
    "status": "ACTIVE",
    "type": "CHECKING",
    "attributes": [
        "TRANSACTIONS",
        "PAYMENT_TO",
        "PAYMENT_FROM",
        "TRANSFER_TO",
        "TRANSFER_FROM",
    ],
    "balance": {
        "currency": "NZD",
        "current": 10.00,
        "available": 10.00,
        "overdrawn": False,
    },
    "meta": {"holder": "MR Q C TOUT"},
    "refreshed": {
        "balance": "2025-02-28T03:16:34.510Z",
        "meta": "2025-02-28T03:16:34.510Z",
        "transactions": "2025-02-28T03:16:41.372Z",
        "party": "2025-02-08T03:46:36.259Z",
    },
}


class TestAccountModel(TestCase):
    def setUp(self):
        self.account = Account(**response, client=None)

    def test_valid_acount_parameters(self):
        account = self.account

        self.assertEqual(account.id, response["_id"])
        self.assertEqual(account.credentials, response["_credentials"])
        self.assertEqual(account.name, response["name"])
        self.assertEqual(account.status, response["status"])
        self.assertEqual(account.formatted_account, response["formatted_account"])
        self.assertDictEqual(account.meta, response["meta"])
        self.assertEqual(account.type, response["type"])
        self.assertListEqual(account.attributes, response["attributes"])

    def test_valid_account_connection_parameters(self):
        connection = self.account.connection
        response_connection = response["connection"]

        self.assertEqual(connection.name, response_connection["name"])
        self.assertEqual(connection.logo, response_connection["logo"])
        self.assertEqual(connection.id, response_connection["_id"])

    def test_valid_account_refreshed_parameters(self):
        refreshed = self.account.refreshed
        response_refreshed = response["refreshed"]

        self.assertEqual(
            Utils.datetime_to_iso(refreshed.balance), response_refreshed["balance"]
        )
        self.assertEqual(
            Utils.datetime_to_iso(refreshed.meta), response_refreshed["meta"]
        )
        self.assertEqual(
            Utils.datetime_to_iso(refreshed.transactions),
            response_refreshed["transactions"],
        )
        self.assertEqual(
            Utils.datetime_to_iso(refreshed.party), response_refreshed["party"]
        )

    def test_valid_account_balance_parameters(self):
        balance = self.account.balance
        response_balance = response["balance"]

        self.assertEqual(balance.current, response_balance["current"])
        self.assertEqual(balance.available, response_balance.get("available"))
        self.assertEqual(balance.limit, response_balance.get("limit"))
        self.assertEqual(balance.overdrawn, response_balance.get("overdrawn"))
        self.assertEqual(balance.currency, response_balance["currency"])
