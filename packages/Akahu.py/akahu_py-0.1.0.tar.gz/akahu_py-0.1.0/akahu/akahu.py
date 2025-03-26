from akahu.rest_adapter import RestAdapter
from akahu.utils import Utils
from akahu.models.account import Account
from akahu.models.transaction import Transaction, PendingTransaction
from akahu.models.payment import Payment
from akahu.decorators import on_cooldown

from typing import List
from datetime import datetime


class Client:
    """Represents a connection to the Akahu API."""

    def __init__(self, app_token: str, user_token: str) -> None:
        """Initializes a client connection.

        Parameters
        ----------
        app_token : str
            An app token provided by Akahu.
        user_token : str
            A user token provided by Akahu.
        """
        headers = {"X-Akahu-Id": app_token, "Authorization": f"Bearer {user_token}"}

        self._rest_adapter: RestAdapter = RestAdapter(
            "https://api.akahu.io/v1", headers=headers
        )

    def get_all_accounts(self) -> List[Account]:
        """Retrieves all accounts connected to your Akahu app.

        Returns
        -------
            List[Account]
                A list of `Account` objects.
        """
        raw_accounts = self._rest_adapter.get("/accounts")["items"]

        return [Account(client=self, **raw_account) for raw_account in raw_accounts]

    def get_account(self, id: str) -> Account:
        """Retrieves a single account based off of its Akahu ID.

        Parameters
        ----------
            id : str
                An Akahu account ID.

        Returns
        -------
            Account
                An `Account` object.
        """
        raw_account = self._rest_adapter.get(f"/account/{id}")["item"]

        return Account(client=self, **raw_account)

    @on_cooldown(seconds=3600)
    def refresh_account(self, id: str = None) -> bool:
        """Refreshes accounts connected to your Akahu app.

        Refreshes the data that pertains to each account connected to your Akahu app.
        This function has an hour cooldown to comply with Akahu's ratelimits. If an ID is
        not given all accounts will be refreshed.

        Parameters
        ----------
            id : str, optional
                An Akahu account ID.

        Returns
        -------
            bool
                A boolean indicating wether the account\s were refreshed.
        """
        if id:
            raw_refresh = self._rest_adapter.post(f"/refresh/{id}")
        else:
            raw_refresh = self._rest_adapter.post("/refresh")

        return raw_refresh["success"]

    def get_transactions(self, start: datetime, end: datetime) -> List[Transaction]:
        """Retrieves all transactions between two points in time.

        Parameters
        ----------
            start : datetime
                A date and time to fetch from.
            end : datetime
                A date and time to fetch to.

        Returns
        -------
            List[Transaction]
                A list of `Transaction` objects.
        """
        params = {
            "start": Utils.datetime_to_iso(start),
            "end": Utils.datetime_to_iso(end),
        }
        raw_transactions = self._rest_adapter.get("/transactions", params=params)[
            "items"
        ]

        return [Transaction(**raw_transaction) for raw_transaction in raw_transactions]

    def get_transaction(self, id: str) -> Transaction:
        """Retrieves a transaction.

        Parameters
        ----------
            id : str
                An Akahu transaction ID.

        Returns
        -------
            Transaction
                An Akahu `Transaction` object.
        """
        raw_transaction = self._rest_adapter.get(f"/transactions/{id}")["item"]

        return Transaction(**raw_transaction)

    def get_pending_transactions(self) -> List[PendingTransaction]:
        """Retrieves pending transactions.

        Returns
        -------
            List[PendingTransaction]
                A list of `PendingTransaction` objects.
        """
        raw_transactions = self._rest_adapter.get("/transactions/pending")["items"]

        return [
            PendingTransaction(**raw_transaction)
            for raw_transaction in raw_transactions
        ]

    def get_payments(self, start: datetime, end: datetime) -> List[Payment]:
        """Retrieves payments between two points in time.

        Fetches payments initiated by your application on behalf of an Akahu user,
        specifically between two points in time.

        Parameters
        ----------
            start : datetime
                A date and time to fetch from.
            end : datetime
                A date and time to fetch to.

        Returns
        -------
            List[Payment]
                A list of `Payment` objects.
        """
        params = {
            "start": Utils.datetime_to_iso(start),
            "end": Utils.datetime_to_iso(end),
        }

        raw_payments = self._rest_adapter.get("/payments", params=params)["items"]

        return [Payment(**raw_payment) for raw_payment in raw_payments]

    def get_payment(self, id: str) -> Payment:
        """Retrieves a payment by its Akahu assigned ID.

        Fetches a payment initiated by your application on behalf of an
        Akahu user.

        Parameters
        ----------
            id : str
                An Akahu payment ID.

        Returns
        -------
            Payment
                A `Payment` object.
        """
        raw_payment = self._rest_adapter.get(f"/payments/{id}")["item"]

        return Payment(**raw_payment)

    def get_transfers(self, start: datetime, end: datetime) -> List[Payment]:
        """Retrieves a list of transfers.

        Fetches a list of transfer that your Akahu application initiated between
        the user's connected accounts between two points in time.

        Parameters
        ----------
            start : datetime
                A date and time to fetch from. Accepted as a `datetime` object.
            end : datetime
                A date and time to fetch to. Accepted as a `datetime` object.

        Returns
        -------
            List[Payment]
                A list of `Payment` objects.
        """
        params = {
            "start": Utils.datetime_to_iso(start),
            "end": Utils.datetime_to_iso(end),
        }

        raw_transfers = self._rest_adapter.get("/transfers", params=params)["items"]

        return [Payment(**raw_transfer) for raw_transfer in raw_transfers]

    def get_transfer(self, id: str) -> Payment:
        """Retrieves a transfer

        Fetches a transfer that your Akahu application initiated between the user's
        connected accounts based of an Akahu assigned ID.

        Parameters
        ----------
            id : str
                An Akahu transfer ID.

        Returns
        -------
            Payment
                A `Payment` object.
        """
        raw_transfer = self._rest_adapter.get(f"/transfers/{id}")["item"]

        return Payment(**raw_transfer)
