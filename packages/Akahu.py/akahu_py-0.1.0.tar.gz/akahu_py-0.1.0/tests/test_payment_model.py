from unittest import TestCase
from datetime import datetime

from akahu.models.payment import Payment
from akahu.utils import Utils

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


class TestPaymentModel(TestCase):
    def setUp(self):
        self.payment = Payment(**response["item"])

    def test_valid_payment_parameters(self):
        payment = self.payment
        payment_response = response["item"]

        self.assertEqual(payment.id, payment_response["_id"])
        self.assertEqual(payment.from_, payment_response["from"])
        self.assertEqual(payment.amount, payment_response["amount"])
        self.assertDictEqual(payment.meta, payment_response["meta"])
        self.assertEqual(payment.sid, payment_response["sid"])
        self.assertEqual(payment.status, payment_response["status"])
        self.assertEqual(payment.status_text, payment_response["status_text"])
        self.assertEqual(payment.final, payment_response["final"])
        self.assertEqual(
            Utils.datetime_to_iso(payment.created_at), payment_response["created_at"]
        )
        self.assertEqual(
            Utils.datetime_to_iso(payment.updated_at), payment_response["updated_at"]
        )
        self.assertEqual(
            Utils.datetime_to_iso(payment.received_at), payment_response["received_at"]
        )

    def test_valid_payment_to_parameters(self):
        to = self.payment.to
        to_response = response["item"]["to"]

        self.assertEqual(to.account_number, to_response["account_number"])
        self.assertEqual(to.name, to_response["name"])

    def test_valid_payment_timeline_parameters(self):
        timeline_response = response["item"]["timeline"]

        for index, timeline in enumerate(self.payment.timeline):
            self.assertEqual(timeline.status, timeline_response[index]["status"])
            self.assertEqual(
                Utils.datetime_to_iso(timeline.time), timeline_response[index]["time"]
            )
            self.assertEqual(
                Utils.datetime_to_iso(timeline.eta), timeline_response[index]["eta"]
            )
