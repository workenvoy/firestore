from datetime import datetime, timezone, timedelta
from iso8601 import parse_date, ParseError

from firestore.errors import ValidationError
from firestore.datatypes.base import Base


class Timestamp(Base):
    """
    Firestore timestamp object. When stored in Cloud Firestore, precise
    only to microseconds; any additional precision is rounded down
    """

    __slots__ = ("value", "_name", "minimum", "maximum", "coerce")

    def __init__(self, *args, **kwargs):
        self.minimum = kwargs.get("minimum")
        self.maximum = kwargs.get("maximum")
        super(Timestamp, self).__init__(*args, **kwargs)

    def do_coercion(self, value):
        """
        Coerce the value provided into the correct underlying type
        for persistence to cloud firestore
        """
        # Timestamps are non alphanumeric collection of numbers so
        # we can use the str isnumeric builtin to differentiate it
        # from the alphanumeric iso8601 format
        if isinstance(value, int) or isinstance(value, float):
            return datetime.fromtimestamp(float(value)).astimezone()

        # Otherwise try to parse from ISO format
        return parse_date(value)

    def validate(self, value):
        # By default values are coerced from timestamp
        # or from iso8601
        if not isinstance(value, datetime):
            try:
                _val = self.do_coercion(value)
            except:
                raise ValueError(f"Could not load {value} into {self._name}")
        else:
            _val = value

        # To avoid repetition a placeholder
        # message for the expected value of timestamp
        min_max_msg = "{} field option must be datetime or coercible to datetime"

        # First we get the minimum value as a datetime object or
        # as a coercible value i.e. timestamp
        # or iso formatted datetime string
        if self.minimum and not isinstance(self.minimum, datetime):
            try:
                _min = self.do_coercion(self.minimum)
            except:
                raise ValueError(min_max_msg.format("Minimum"))
            if _val < _min:
                raise ValidationError(f"Date must be greater than {self.maximum}")

        # Next we get the maximum value if the maximum attribute
        # was specified and coerce then compare
        # appropriately
        if self.maximum and not isinstance(self.maximum, datetime):
            try:
                _max = self.do_coercion(self.maximum)
            except:
                raise ValueError(min_max_msg.format("Maximum"))
            if _val > _max:
                raise ValidationError(f"Date must be greater than {self.maximum}")

        return _val
