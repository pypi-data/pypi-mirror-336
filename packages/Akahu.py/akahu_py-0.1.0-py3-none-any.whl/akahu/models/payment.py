from datetime import datetime
from typing import List

from akahu.utils import Utils


class To:
    """A representation of the receivers information.

    Attributes
    ----------
    account_number : str
        An Akahu account ID.
    name : str
        The name of the destination account.
    """

    def __init__(self, account_number: str, name: str):
        """Initializes a `To` object.

        Parameters
        ----------
        account_number : str
            An Akahu account ID.
        name : str
            The name of the destination account.
        """
        self.account_number: str = account_number
        self.name: str = name


class Timeline:
    """A representation of a point in a payments timeline.

    Attributes
    ----------
    status : str
        The status of this payment at this point
    time : datetime
        The time of this point.
    eta : datetime, optional
        The time that Akahu expect the payment to arrive, by deafult None.
    """

    def __init__(self, status: str, time: str, eta: str = None):
        """Initializes a `Timeline` object

        Parameters
        ----------
        status : str
            The status of this payment at this point.
        time : str
            The time of this point.
        eta : str, optional
            The time that Akahu expect the payment to arrive, by deafult None.
        """
        self.status: str = status
        self.time: datetime = Utils.iso_to_datetime(time)
        self.eta: datetime = Utils.iso_to_datetime(eta) if eta else None


class Payment:
    """A representation of an Akahu payment.

    Attributes
    ----------
    id : str
        A payment id.
    to : `To`
        A `To` object with information about the payee.
    from\_ : str
        The ID of the source account.
    amount : int
        The amount paid.
    sid : str
        A unique Akahu ID inserted into the `particulars` field.
    status : str
        Status of the payment.
    final : bool
        Wether the payment has reached its final state.
    timeline : List[Timeline]
        A list of `Timeline` objects detailing a payments timeline.
    created_at : datetime
        When the payment was created.
    updated_at : datetime
        When this payment was last update by Akahu
    meta : dict, optional
        Payment metadata, by default None.
    status_text : str, optional
        More information about the payments status, by default None.
    received_at : datetime, optional
        When this payment was recieved by the destination account, by default None.
    """

    def __init__(
        self,
        _id: str,
        to: dict,
        amount: int,
        sid: str,
        status: str,
        final: bool,
        timeline: list,
        created_at: str,
        updated_at: str,
        meta: dict = None,
        status_text: str = None,
        received_at: str = None,
        **kwargs
    ):
        """Initializes a `Payment` object.

        Parameters
        ----------
        _id : str
            A payment id.
        to : dict
            Information on the recipient.
        from_ : str
            The ID of the source account.
        amount : int
            The amount paid.
        sid : str
            A unique Akahu ID inserted into the `particulars` field.
        status : str
            Status of the payment.
        final : bool
            Wether the payment has reached its final state.
        timeline : list
            Information about the timeline of this payment.
        created_at : str
            When the payment was created.
        updated_at : str
            When this payment was last update by Akahu
        meta : dict, optional
            Payment metadata, by default None.
        status_text : str, optional
            More information about the payments status, by default None.
        received_at : str, optional
            When this payment was recieved by the destination account, by default None.
        """
        self._id = _id
        self.from_ = kwargs.pop("from")
        self.to = to if isinstance(to, str) else To(**to)
        self.amount: int = amount
        self.meta: dict = meta
        self.sid: str = sid
        self.status: str = status
        self.status_text: str = status_text
        self.final: bool = final
        self.timeline: List[Timeline] = [Timeline(**line) for line in timeline]
        self.created_at: datetime = Utils.iso_to_datetime(created_at)
        self.updated_at: datetime = Utils.iso_to_datetime(updated_at)
        self.received_at: datetime = (
            Utils.iso_to_datetime(received_at) if received_at else None
        )

    @property
    def id(self):
        return self._id
