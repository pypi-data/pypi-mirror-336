from datetime import datetime


class Utils:
    @staticmethod
    def iso_to_datetime(str: str) -> datetime:
        return datetime.fromisoformat(str)

    @staticmethod
    def datetime_to_iso(datetime: datetime) -> str:
        return datetime.strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + "Z"

    @staticmethod
    def object_to_dict(obj: dict, remove_none=False) -> dict:
        object_dict = {}

        for attribute_key, attribute_value in vars(obj).items():
            if hasattr(attribute_value, "__dict__"):
                object_dict[attribute_key] = Utils.object_to_dict(
                    attribute_value, remove_none=remove_none
                )
            elif isinstance(attribute_value, list):
                object_dict[attribute_key] = [
                    (
                        Utils.object_to_dict(item, remove_none=remove_none)
                        if hasattr(item, "__dict__")
                        else item
                    )
                    for item in attribute_value
                ]
            elif isinstance(attribute_value, datetime):
                object_dict[attribute_key] = Utils.datetime_to_iso(attribute_value)
            elif remove_none and attribute_value is None:
                continue
            else:
                object_dict[attribute_key] = attribute_value

        return object_dict
