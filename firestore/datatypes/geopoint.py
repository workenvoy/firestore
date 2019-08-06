from firestore.datatypes.base import Base


MAX_LATITUDE = 90.0
MIN_LATITUDE = -90.0

MAX_LONGITUDE = MAX_LATITUDE * 2
MIN_LONGITUDE = MIN_LATITUDE * 2


class Geopoint(Base):
    """
    Geographic coordinates

    Organised by latitude, then longitude
    """

    def __init__(self, *args, **kwargs):
        default = kwargs.get("default")
        if default:
            self.validate(default)

        super(Geopoint, self).__init__(*args, **kwargs)

    def validate(self, value):
        if not isinstance(value, (list, tuple)):
            raise ValueError(
                "Unsupported value assigned to Geopoint - only list, tuple supported"
            )
        if len(value) != 2:
            raise ValueError(
                "Geopoint requires exactly two values for latitude and longitude"
            )

        latitude, longitude = value

        if (
            not isinstance(latitude, (int, float))
            or latitude < MIN_LATITUDE
            or latitude > MAX_LATITUDE
        ):
            raise ValueError(f"Invalid latitude value {latitude} detected")
        if (
            not isinstance(longitude, (int, float))
            or longitude < MIN_LONGITUDE
            or longitude > MAX_LONGITUDE
        ):
            raise ValueError("Invalid longitude value detected")

        self.latitude, self.longitude = value
