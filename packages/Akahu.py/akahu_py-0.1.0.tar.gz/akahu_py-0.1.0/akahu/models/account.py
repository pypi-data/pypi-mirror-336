from akahu.models.payment import Payment
from akahu.models.transaction import Transaction, PendingTransaction
from akahu.utils import Utils

from typing import List
from datetime import datetime


class Connection:
    """A representation of an account connection.

    Attributes
    ----------
    name : str
        The name of the connection.
    logo : str
        The uri of the connection logo.
    id : str
        The ID of the connection
    """
    def __init__(self, name: str, logo: str, _id: str) -> None:
        """Initializes a `Connection` object.

        Parameters
        ----------
        name : str
            The name of the connection.
        logo : str
            The uri of the connection logo.
        _id : str
            The ID of the connection
        """
        self.name: str = name
        self.logo: str = logo
        self._id: str = _id

    @property
    def id(self):
        return self._id


class Refreshed:
    """A representation of when data was last refreshed.

    Attributes
    ----------
    balance : datetime
        The time when the balance was last updated.
    meta : datetime
        The time when the metadata was last updated.
    party : datetime
        The time when the party was last updated.
    transactions : datetime, optional
        The time when the transactions was last updated, by default None.
    """
    def __init__(
        self, balance: str, meta: str, party: str, transactions: str = None
    ) -> None:
        """Initializes a `Refreshed` object.

        Parameters
        ----------
        balance : str
            The time when the balance was last updated.
        meta : str
            The time when the metadata was last updated.
        party : str
            The time when the party was last updated.
        transactions : str, optional
            The time when the transactions was last updated, by default None.
        """
        self.balance: datetime = Utils.iso_to_datetime(balance)
        self.meta: str = Utils.iso_to_datetime(meta)
        self.transactions: str = Utils.iso_to_datetime(transactions)
        self.party: str = Utils.iso_to_datetime(party)


class Balance:
    """A representation of an `Account` balance.

    Attributes
    ----------
    current : float
        The current account balance.
    currency : str
        The currency the balance is in.
    available : float, optional
        The balance that is available to the account holder, by default None.
    limit : float, optional
        The credit limit for this account, by default None.
    overdrawn : bool, optional
        Wether the account is overdrawn or not, by default None.
    """
    def __init__(
        self,
        current: float,
        currency: str,
        available: float = None,
        limit: float = None,
        overdrawn: bool = None,
    ) -> None:
        """Initializes a `Balance` object.

        Parameters
        ----------
        current : float
            The current account balance.
        currency : str
            The currency the balance is in.
        available : float, optional
            The balance that is available to the account holder, by default None.
        limit : float, optional
            The credit limit for this account, by default None.
        overdrawn : bool, optional
            Wether the account is overdrawn or not, by default None.
        """
        self.current: float = current
        self.available: float = available
        self.limit: float = limit
        self.overdrawn: bool = overdrawn
        self.currency: str = currency


class Account:
    """A representation of an Akahu account.

    Attributes
    ----------
    id : str
        An Akahu acount ID.
    credentials : str
        Akahu credentials key.
    connection : `Connection`
        Information about account issuer.
    name : str
        Account name.
    status : str
        Connection status.
    balance : `Balance`
        Information about the accounts balance.
    type : str
        Type of account.
    attributes : List[Str]
        A list of the account's abilities.
    refreshed : `Refreshed`, optional
        Information on when the account and its attributes was last refreshed, by default None.
    formatted_account : str, optional
        An accounts well defined account number (bank account number, credit card number), by default None.
    meta :  dict, optional
        Miscellaneous *non-standard* information about the account, by default None.
    """

    def __init__(
        self,
        _id: str,
        _credentials: str,
        connection: dict,
        name: str,
        status: str,
        balance: dict,
        type: str,
        attributes: List[str],
        client,
        refreshed: dict = None,
        formatted_account: str = None,
        meta: dict = None,
    ) -> None:
        """Initializes an `Account` object.

        Parameters
        ----------
        _id : str
            Akahu account ID.
        _credentials : str
            Akahu credentials key.
        connection : dict
            Information about account issuer.
        name : str
            Account name.
        status : str
            Connection status.
        balance : dict
            Information about the accounts balance.
        type : str
            Type of account.
        attributes : List[str]
            Account's abilities.
        client : _type_
            `Client` object the account was retrieved from.
        refreshed : dict, optional
            Information on when the account and its attributes was last refreshed, by default None.
        formatted_account : str, optional
            An accounts well defined account number (bank account number, credit card number), by default None.
        meta : dict, optional
            Miscellaneous *non-standard* information about the account, by default None.
        """
        self._id: str = _id
        self._credentials: str = _credentials
        self.connection: Connection = Connection(**connection)
        self.name: str = name
        self.status: str = status
        self.formatted_account: str = formatted_account
        self.meta: dict = meta
        self.refreshed = Refreshed(**refreshed)
        self.balance: Balance = Balance(**balance)
        self.type: str = type
        self.attributes: List[str] = attributes

        from akahu.akahu import Client

        self._client: Client = client

    @property
    def id(self):
        return self._id

    @property
    def credentials(self):
        return self._credentials

    def make_payment(
        self,
        name: str,
        account_number: str,
        amount: float,
        source_code: str = None,
        source_reference: str = None,
        destination_particulars: str = None,
        destination_code: str = None,
        destination_reference: str = None,
    ) -> Payment:
        """Make a payment from this `Account` object.

        Parameters
        ----------
        name : str
            Name of the payee.
        account_number : str
            Account number of the payee.
        amount : float
            Amount to be paid.
        source_code : str, optional
            Code for the payer, by default None.
        source_reference : str, optional
            Reference for the payer, by default None.
        destination_particulars : str, optional
            Particulars for the payee, by default None.
        destination_code : str, optional
            Code for the payee, by default None.
        destination_reference : str, optional
            Reference for the payee, by default None.

        Returns
        -------
        Payment
            A `Payment` object.
        """
        params = {
            "from": self.id,
            "to": {"name": name, "account_number": account_number},
            "amount": amount,
            "meta": {
                "source": {"code": source_code, "reference": source_reference},
                "destination": {
                    "particulars": destination_particulars,
                    "code": destination_code,
                    "reference": destination_reference,
                },
            },
        }

        raw_payment = self._client._rest_adapter.post("/payments", json=params)["item"]

        return Payment(**raw_payment)

    def make_transfer(self, to: str, amount: float) -> Payment:
        """Transfer funds between two accounts

        Transfer funds from this `Account` object to another account. Both
        accounts **must** be connected to your Akahu app.

        Parameters
        ----------
        to : str
            The account to transfer to.
        amount : float
            The amount to be transferred.

        Returns
        -------
        Payment
            A `Payment` object.
        """
        params = {"from": self.id, "to": to, "amount": amount}

        raw_payment = self._client._rest_adapter.post("/transfers", json=params)["item"]

        return Payment(**raw_payment)

    def get_transactions(
        self, start: datetime = None, end: datetime = None
    ) -> List[Transaction]:
        """Retrieves a transaction connected to this `Acount` object.

        Parameters
        ----------
        start : datetime, optional
            A datetime to fetch from, by default None.
        end : datetime, optional
            A datetime to fetch to, by default None.

        Returns
        -------
        List[Transaction]
            A list of `Transaction` objects.
        """
        if start and end:
            params = {"start": start, "end": end}
        else:
            params = None

        raw_transactions = self._client._rest_adapter.get(
            f"/accounts/{self.id}/transactions", json=params
        )["items"]

        return [Transaction(**raw_transaction) for raw_transaction in raw_transactions]

    def get_pending_transactions(self) -> List[PendingTransaction]:
        """Get all pending transaction connected to this `Account` object.

        Returns
        -------
        List[PendingTransaction]
            A list of `PendingTransaction` objects.
        """
        raw_transactions = self._client._rest_adapter.get(
            f"/accounts/{self.id}/transactions/pending"
        )["items"]

        return [
            PendingTransaction(**raw_transaction)
            for raw_transaction in raw_transactions
        ]
