from unittest import TestCase, mock
from datetime import datetime

from akahu.akahu import Client
from akahu.utils import Utils
from akahu.models.transaction import Transaction


class TestClient(TestCase):
    def setUp(self):
        self.client = Client("", "")
        self.maxDiff = None

    def test_get_all_accounts_valid(self):
        response = {
            "success": True,
            "items": [
                {
                    "_id": "acc_1111111111111111111111111",
                    "_credentials": "creds_1111111111111111111111111",
                    "connection": {
                        "_id": "conn_1111111111111111111111111",
                        "name": "ANZ",
                        "logo": "https://cdn.akahu.nz/logos/connections/conn_cjgaawozb000001nyd111xixr",
                    },
                    "name": "Demo Account",
                    "status": "ACTIVE",
                    "balance": {
                        "currency": "NZD",
                        "current": 99.9,
                        "available": 99.9,
                        "limit": 1000,
                        "overdrawn": False,
                    },
                    "type": "CHECKING",
                    "attributes": [
                        "TRANSFER_TO",
                        "PAYMENT_TO",
                        "TRANSACTIONS",
                        "PAYMENT_FROM",
                        "TRANSFER_FROM",
                    ],
                    "formatted_account": "12-1234-1234567-12",
                    "meta": {
                        "holder": "MR DEMO HOLDER & MS DEMO HOLDER",
                        "loan_details": {
                            "purpose": "HOME",
                            "type": "TABLE",
                            "interest": {
                                "rate": 4.5,
                                "type": "FIXED",
                                "expires_at": "2021-01-01T12:00:00.000Z",
                            },
                            "is_interest_only": False,
                            "interest_only_expires_at": "2021-01-01T12:00:00.000Z",
                            "term": {"years": 30, "months": 5},
                            "matures_at": "2021-01-01T12:00:00.000Z",
                            "initial_principal": 100000,
                            "repayment": {
                                "frequency": "MONTHLY",
                                "next_date": "2021-01-01T12:00:00.000Z",
                                "next_amount": 1000,
                            },
                        },
                        "additionalProp": {},
                    },
                    "refreshed": {
                        "balance": "2021-01-01T12:00:00.000Z",
                        "meta": "2021-01-01T12:00:00.000Z",
                        "transactions": "2021-01-01T12:00:00.000Z",
                        "party": "2021-01-01T12:00:00.000Z",
                    },
                }
            ],
        }

        with mock.patch("akahu.rest_adapter.RestAdapter.get", return_value=response):
            result = self.client.get_all_accounts()

        for account, raw_account in zip(result, response["items"]):
            account_dict = Utils.object_to_dict(account)
            account_dict.pop("_client")

            self.assertDictEqual(account_dict, raw_account)

    def test_get_account_valid(self):
        response = {
            "success": True,
            "item": {
                "_id": "acc_1111111111111111111111111",
                "_credentials": "creds_1111111111111111111111111",
                "connection": {
                    "_id": "conn_1111111111111111111111111",
                    "name": "ANZ",
                    "logo": "https://cdn.akahu.nz/logos/connections/conn_cjgaawozb000001nyd111xixr",
                },
                "name": "Demo Account",
                "status": "ACTIVE",
                "balance": {
                    "currency": "NZD",
                    "current": 99.9,
                    "available": 99.9,
                    "limit": 1000,
                    "overdrawn": False,
                },
                "type": "CHECKING",
                "attributes": [
                    "TRANSFER_TO",
                    "PAYMENT_TO",
                    "TRANSACTIONS",
                    "PAYMENT_FROM",
                    "TRANSFER_FROM",
                ],
                "formatted_account": "12-1234-1234567-12",
                "meta": {
                    "holder": "MR DEMO HOLDER & MS DEMO HOLDER",
                    "loan_details": {
                        "purpose": "HOME",
                        "type": "TABLE",
                        "interest": {
                            "rate": 4.5,
                            "type": "FIXED",
                            "expires_at": "2021-01-01T12:00:00.000Z",
                        },
                        "is_interest_only": False,
                        "interest_only_expires_at": "2021-01-01T12:00:00.000Z",
                        "term": {"years": 30, "months": 5},
                        "matures_at": "2021-01-01T12:00:00.000Z",
                        "initial_principal": 100000,
                        "repayment": {
                            "frequency": "MONTHLY",
                            "next_date": "2021-01-01T12:00:00.000Z",
                            "next_amount": 1000,
                        },
                    },
                    "additionalProp": {},
                },
                "refreshed": {
                    "balance": "2021-01-01T12:00:00.000Z",
                    "meta": "2021-01-01T12:00:00.000Z",
                    "transactions": "2021-01-01T12:00:00.000Z",
                    "party": "2021-01-01T12:00:00.000Z",
                },
            },
        }

        with mock.patch("akahu.rest_adapter.RestAdapter.get", return_value=response):
            result = self.client.get_account("")

        account_dict = Utils.object_to_dict(result)
        account_dict.pop("_client")

        self.assertDictEqual(account_dict, response["item"])

    def test_refresh_accounts_success(self):
        response = {"success": True}

        with (
            mock.patch("akahu.rest_adapter.RestAdapter.post", return_value=response),
            mock.patch(
                "akahu.decorators.on_cooldown", lambda seconds: (lambda func: func)
            ),
        ):
            result = self.client.refresh_account()

        self.assertEqual(result, response["success"])

    def test_refresh_accounts_fail(self):
        response = {"success": False}

        with (
            mock.patch("akahu.rest_adapter.RestAdapter.post", return_value=response),
            mock.patch(
                "akahu.decorators.on_cooldown", lambda seconds: (lambda func: func)
            ),
        ):
            result = self.client.refresh_account()

        self.assertEqual(result, response["success"])

    def test_get_transactions_unenriched_valid(self):
        response = {
            "success": True,
            "cursor": {"next": "abc123"},
            "items": [
                {
                    "_id": "trans_1111111111111111111111111",
                    "_account": "acc_1111111111111111111111111",
                    "_connection": "conn_1111111111111111111111111",
                    "created_at": "2020-01-01T01:00:00.000Z",
                    "updated_at": "2020-01-01T01:00:00.000Z",
                    "date": "2020-01-01T00:00:00.000Z",
                    "description": "{RAW TRANSACTION DESCRIPTION}",
                    "amount": -5.5,
                    "balance": 100,
                    "type": "EFTPOS",
                }
            ],
        }

        with mock.patch("akahu.rest_adapter.RestAdapter.get", return_value=response):
            result = self.client.get_transactions(
                datetime.fromtimestamp(1741564637), datetime.fromtimestamp(1741564636)
            )

        for transaction, raw_transaction in zip(result, response["items"]):
            self.assertDictEqual(
                raw_transaction, Utils.object_to_dict(transaction, remove_none=True)
            )

    def test_get_transactions_enriched_valid(self):
        response = {
            "success": True,
            "cursor": {"next": "abc123"},
            "items": [
                {
                    "_id": "trans_1111111111111111111111111",
                    "_account": "acc_1111111111111111111111111",
                    "_connection": "conn_1111111111111111111111111",
                    "created_at": "2020-01-01T01:00:00.000Z",
                    "updated_at": "2020-01-01T01:00:00.000Z",
                    "date": "2020-01-01T00:00:00.000Z",
                    "description": "{RAW TRANSACTION DESCRIPTION}",
                    "amount": -5.5,
                    "balance": 100,
                    "type": "EFTPOS",
                    "merchant": {
                        "_id": "merchant_1111111111111111111111111",
                        "name": "Bob's Pizza",
                    },
                    "category": {
                        "_id": "nzfcc_1111111111111111111111111",
                        "name": "Cafes and restaurants",
                        "groups": {
                            "personal_finance": {
                                "_id": "group_clasr0ysw0011hk4m6hlk9fq0",
                                "name": "Lifestyle",
                            }
                        },
                    },
                    "meta": {
                        "logo": "https://static.akahu.io/avatars/P.png",
                        "particulars": "...",
                        "code": "...",
                        "reference": "...",
                        "other_account": "00-0000-0000000-00",
                        "conversion": {"amount": 2, "currency": "GBP", "rate": 2.75},
                        "card_suffix": "1234",
                    },
                }
            ],
        }

        [item.pop("category") for item in response["items"]]  # Naughty, I know.

        with mock.patch("akahu.rest_adapter.RestAdapter.get", return_value=response):
            result = self.client.get_transactions(
                datetime.fromtimestamp(1741564637), datetime.fromtimestamp(1741564636)
            )

        for transaction, raw_transaction in zip(result, response["items"]):
            self.assertDictEqual(
                raw_transaction, Utils.object_to_dict(transaction, remove_none=True)
            )

    def test_get_transaction_unenriched_valid(self):
        response = {
            "success": True,
            "item": {
                "_id": "trans_1111111111111111111111111",
                "_account": "acc_1111111111111111111111111",
                "_connection": "conn_1111111111111111111111111",
                "created_at": "2020-01-01T01:00:00.000Z",
                "updated_at": "2020-01-01T01:00:00.000Z",
                "date": "2020-01-01T00:00:00.000Z",
                "description": "{RAW TRANSACTION DESCRIPTION}",
                "amount": -5.5,
                "balance": 100,
                "type": "EFTPOS",
            },
        }

        with mock.patch("akahu.rest_adapter.RestAdapter.get", return_value=response):
            result = self.client.get_transaction("")

        self.assertDictEqual(
            response["item"], Utils.object_to_dict(result, remove_none=True)
        )

    def test_get_transaction_enriched_valid(self):
        response = {
            "success": True,
            "item": {
                "_id": "trans_1111111111111111111111111",
                "_account": "acc_1111111111111111111111111",
                "_connection": "conn_1111111111111111111111111",
                "created_at": "2020-01-01T01:00:00.000Z",
                "updated_at": "2020-01-01T01:00:00.000Z",
                "date": "2020-01-01T00:00:00.000Z",
                "description": "{RAW TRANSACTION DESCRIPTION}",
                "amount": -5.5,
                "balance": 100,
                "type": "EFTPOS",
                "merchant": {
                    "_id": "merchant_1111111111111111111111111",
                    "name": "Bob's Pizza",
                },
                "category": {
                    "_id": "nzfcc_1111111111111111111111111",
                    "name": "Cafes and restaurants",
                    "groups": {
                        "personal_finance": {
                            "_id": "group_clasr0ysw0011hk4m6hlk9fq0",
                            "name": "Lifestyle",
                        }
                    },
                },
            },
        }

        response["item"].pop("category")  # Naughty, I know.

        with mock.patch("akahu.rest_adapter.RestAdapter.get", return_value=response):
            result = self.client.get_transaction("")

        self.assertDictEqual(
            response["item"], Utils.object_to_dict(result, remove_none=True)
        )

    def test_get_pending_transactions_valid(self):
        response = {
            "success": True,
            "items": [
                {
                    "_account": "acc_1111111111111111111111111",
                    "_connection": "conn_1111111111111111111111111",
                    "_user": "user_1111111111111111111111111",
                    "updated_at": "2020-01-01T01:00:00.000Z",
                    "date": "2020-01-01T01:00:00.000Z",
                    "description": "{ RAW TRANSACTION DESCRIPTION }",
                    "amount": -5.5,
                    "type": "EFTPOS",
                }
            ],
        }

        with mock.patch("akahu.rest_adapter.RestAdapter.get", return_value=response):
            result = self.client.get_pending_transactions()

        for transaction, raw_transaction in zip(result, response["items"]):
            self.assertDictEqual(
                raw_transaction, Utils.object_to_dict(transaction, remove_none=True)
            )

    def test_get_payments_valid(self):
        response = {
            "success": True,
            "items": [
                {
                    "_id": "payment_1111111111111111111111111",
                    "from": "acc_1111111111111111111111111",
                    "to": {
                        "account_number": "12-1234-1234567-12",
                        "name": "John Smith",
                    },
                    "amount": 9.51,
                    "meta": {
                        "destination": {
                            "particulars": "destPart",
                            "code": "destCode",
                            "reference": "destRef",
                        },
                        "source": {"code": "sourceCode", "reference": "sourceRef"},
                    },
                    "sid": "akp111111111",
                    "status": "READY",
                    "status_text": "This payment has just been created and is ready to be sent",
                    "final": False,
                    "timeline": [
                        {
                            "status": "READY",
                            "time": "2020-01-01T01:00:00.000Z",
                            "eta": "2020-01-01T01:00:00.000Z",
                        }
                    ],
                    "created_at": "2020-01-01T01:00:00.000Z",
                    "updated_at": "2020-01-01T01:00:00.000Z",
                    "received_at": "2020-01-01T01:00:00.000Z",
                }
            ],
        }

        with mock.patch("akahu.rest_adapter.RestAdapter.get", return_value=response):
            result = self.client.get_payments(
                datetime.fromtimestamp(1741564637), datetime.fromtimestamp(1741564636)
            )

        for payment, raw_payment in zip(result, response["items"]):
            raw_payment["from_"] = raw_payment.pop("from")
            self.assertDictEqual(
                raw_payment, Utils.object_to_dict(payment, remove_none=True)
            )

    def test_get_payment_valid(self):
        response = {
            "success": True,
            "item": {
                "_id": "payment_1111111111111111111111111",
                "from": "acc_1111111111111111111111111",
                "to": {"account_number": "12-1234-1234567-12", "name": "John Smith"},
                "amount": 9.51,
                "meta": {
                    "destination": {
                        "particulars": "destPart",
                        "code": "destCode",
                        "reference": "destRef",
                    },
                    "source": {"code": "sourceCode", "reference": "sourceRef"},
                },
                "sid": "akp111111111",
                "status": "READY",
                "status_text": "This payment has just been created and is ready to be sent",
                "final": False,
                "timeline": [
                    {
                        "status": "READY",
                        "time": "2020-01-01T01:00:00.000Z",
                        "eta": "2020-01-01T01:00:00.000Z",
                    }
                ],
                "created_at": "2020-01-01T01:00:00.000Z",
                "updated_at": "2020-01-01T01:00:00.000Z",
                "received_at": "2020-01-01T01:00:00.000Z",
            },
        }

        with mock.patch("akahu.rest_adapter.RestAdapter.get", return_value=response):
            result = self.client.get_payment("")

        response["item"]["from_"] = response["item"].pop("from")
        self.assertDictEqual(response["item"], Utils.object_to_dict(result))

    def test_get_transfers_valid(self):
        response = {
            "success": True,
            "items": [
                {
                    "_id": "transfer_1111111111111111111111111",
                    "from": "acc_1111111111111111111111111",
                    "to": "acc_2222222222222222222222222",
                    "amount": 5.5,
                    "sid": "akx111111111",
                    "status": "READY",
                    "status_text": "This transfer has just been created and is ready to be sent",
                    "final": False,
                    "created_at": "2020-04-15T23:12:01.746Z",
                    "updated_at": "2020-04-15T23:12:01.746Z",
                    "timeline": [
                        {"status": "READY", "time": "2020-04-15T23:00:00.000Z"},
                        {"status": "SENT", "time": "2020-04-15T23:01:00.000Z"},
                        {"status": "RECEIVED", "time": "2020-04-15T23:01:07.000Z"},
                    ],
                }
            ],
        }

        with mock.patch("akahu.rest_adapter.RestAdapter.get", return_value=response):
            result = self.client.get_transfers(
                datetime.fromtimestamp(1741564637), datetime.fromtimestamp(1741564636)
            )

        for transfer, raw_transfer in zip(result, response["items"]):
            raw_transfer["from_"] = raw_transfer.pop("from")
            self.assertDictEqual(
                raw_transfer, Utils.object_to_dict(transfer, remove_none=True)
            )

    def test_get_transfer_valid(self):
        response = {
            "success": True,
            "item": {
                "_id": "transfer_1111111111111111111111111",
                "from": "acc_1111111111111111111111111",
                "to": "acc_2222222222222222222222222",
                "amount": 5.5,
                "sid": "akx111111111",
                "status": "READY",
                "status_text": "This transfer has just been created and is ready to be sent",
                "final": False,
                "created_at": "2020-04-15T23:12:01.746Z",
                "updated_at": "2020-04-15T23:12:01.746Z",
                "timeline": [
                    {"status": "READY", "time": "2020-04-15T23:00:00.000Z"},
                    {"status": "SENT", "time": "2020-04-15T23:01:00.000Z"},
                    {"status": "RECEIVED", "time": "2020-04-15T23:01:07.000Z"},
                ],
            },
        }

        with mock.patch("akahu.rest_adapter.RestAdapter.get", return_value=response):
            result = self.client.get_transfer("")

        response["item"]["from_"] = response["item"].pop("from")
        self.assertDictEqual(
            response["item"], Utils.object_to_dict(result, remove_none=True)
        )
