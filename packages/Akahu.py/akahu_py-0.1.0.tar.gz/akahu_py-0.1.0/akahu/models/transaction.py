from akahu.utils import Utils

from typing import List
from datetime import datetime


class Merchant:
    """A representation of an Akahu merchant.

    Attributes
    ----------
    id : str
        The Akahu merchant ID.
    name : str
        The merchant's name.
    website : str, optional
        The merchant's website, by default None.
    nzbn : int, optional
        The merchant's NZBN, by default None.
    """

    def __init__(
        self, _id: str, name: str, website: str = None, nzbn: int = None
    ) -> None:
        """Initializes an Akahu merchant

        Parameters
        ----------
        _id : str
            The Akahu merchant ID.
        name : str
            The merchant's name.
        website : str, optional
            The merchant's website, by default None.
        nzbn : int, optional
            The merchant's NZBN, by default None.
        """
        self._id: str = _id
        self.name: str = name
        self.website: str = website
        self.nzbn: int = nzbn

    @property
    def id(self):
        return self._id


class Category:
    """A representation of an Akahu category

    Attributes
    ----------
    id : str
        A category ID.
    name : str
        The name of the category.
    groups : `Group`
        A `Group` object.
    """

    def __init__(self, _id: str, name: str, groups: dict) -> None:
        """Initializes an Akahu category.

        Parameters
        ----------
        _id : str
            A category ID.
        name : str
            The name of the category.
        groups : dict
            A dictionary of groups.
        """
        self._id: str = _id
        self.name: str = name
        self.groups: List[Group] = [Group(group, **groups[group]) for group in groups]

    @property
    def id(self):
        return self._id


class Group:
    """A representation of an Akahu group

    Attributes
    ----------
    group_name : str
        The name of the group.
    id : str
        The ID of the group.
    name : str
        The name of the sub-group.
    """

    def __init__(self, group_name: str, _id: str, name: str):
        """_summary_

        Parameters
        ----------
        group_name : str
            The name of the group.
        _id : str
            The ID of the group.
        name : str
            The name of the sub-group.
        """
        self.group_name = group_name
        self._id: str = _id
        self.name: str = name

    @property
    def id(self):
        return self._id


class Transaction:
    """
    Attributes
    ----------
    id : str
        The Akahu transaction ID.
    account : str
        The account ID this transaction belongs to.
    connection : str
        The Akahu connection ID that this transaction belongs to.
    created_at : datetime
        The time this transaction was retrieved and created by Akahu.
    updated_at : datetime
        The time this transaction was last updated by Akahu.
    date : datetime
        The time when this transaction was created by the account issuer.
    description : str
        The raw transaction description.
    amount : float
        The amount of funds this transaction was for.
    balance : float
        The balance of the account after this transaction.
    type : str
        The type of transaction.
    user : str, optional
        The Akahu user ID this transaction belongs to, by default None
    meta : dict, optional
        Metadata about this transaction, by default None
    merchant : `Merchant`, optional
        Data about the merchant this transaction was with, by default None
    category : `Category`, optional
        The grouping this transaction belongs to, by default None
    """

    def __init__(
        self,
        _id: str,
        _account: str,
        _connection: str,
        created_at: str,
        updated_at: str,
        date: str,
        description: str,
        amount: float,
        balance: float,
        type: str,
        _user: str = None,
        meta: dict = None,
        merchant: dict = None,
        category: dict = None,
        **kwargs
    ) -> None:
        """Initializes a `Transaction` object.

        Parameters
        ----------
        _id : str
            The Akahu transaction ID.
        _account : str
            The account ID this transaction belongs to.
        _connection : str
            The Akahu connection ID that this transaction belongs to.
        created_at : str
            The time this transaction was retrieved and created by Akahu.
        updated_at : str
            The time this transaction was last updated by Akahu.
        date : str
            The time when this transaction was created by the account issuer.
        description : str
            The raw transaction description.
        amount : float
            The amount of funds this transaction was for.
        balance : float
            The balance of the account after this transaction.
        type : str
            The type of transaction.
        _user : str, optional
            The Akahu user ID this transaction belongs to, by default None
        meta : dict, optional
            Metadata about this transaction, by default None
        merchant : dict, optional
            Data about the merchant this transaction was with, by default None
        category : dict, optional
            The grouping this transaction belongs to, by default None
        """
        self._id: str = _id
        self._account: str = _account
        self._user: str = _user
        self._connection: str = _connection
        self.created_at: datetime = Utils.iso_to_datetime(created_at)
        self.updated_at: datetime = Utils.iso_to_datetime(updated_at)
        self.date: datetime = Utils.iso_to_datetime(date)
        self.description: str = description
        self.amount: float = amount
        self.balance: float = balance
        self.type: str = type
        self.meta: dict = meta

        if merchant:
            self.merchant: Merchant = Merchant(**merchant)
        else:
            self.merchant = None

        if category:
            self.category: Category = Category(**category)
        else:
            self.category = None

    @property
    def id(self):
        return self._id

    @property
    def account(self):
        return self._account

    @property
    def user(self):
        return self._user

    @property
    def connection(self):
        return self._connection


class PendingTransaction:
    def __init__(
        self,
        _account: str,
        _connection: str,
        _user: str,
        updated_at: str,
        date: str,
        description: str,
        amount: float,
        type: str,
    ):
        self._account: str = _account
        self._connection: str = _connection
        self._user: str = _user
        self.updated_at: datetime = Utils.iso_to_datetime(updated_at)
        self.date: datetime = Utils.iso_to_datetime(date)
        self.description: str = description
        self.amount: float = amount
        self.type: str = type

    @property
    def account(self):
        return self._account

    @property
    def connection(self):
        return self._connection

    @property
    def user(self):
        return self._user
