from datetime import datetime, timezone
from google.protobuf import timestamp_pb2
from tzlocal import get_localzone


def datetime_now() -> datetime:
    """
    Plain `datetime.now()` calls will return `datetime` objects without timezone information. In Python, such a
    "naive" `datetime` normally represents local time, but can lead to confusion in distributed settings when
    the `datetime` could also reasonably be interpreted as representing UTC. To disambiguate, Reboot always
    sets the timezone in all `datetime` objects.
    """
    return datetime.now(get_localzone())


def proto_timestamp_to_datetime(
    proto_timestamp: timestamp_pb2.Timestamp
) -> datetime:
    """
    By default, proto's `ToDatetime()` will return a `datetime` object without timezone information; this is incorrect!
    The proto `Timestamp` is explicitly specified as being in UTC, but a Python `datetime` without timezone is
    seen as being in local time! We must explicitly attach the timezone information.
    """
    return proto_timestamp.ToDatetime().replace(tzinfo=timezone.utc)
