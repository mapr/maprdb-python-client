import constants


class OInterval:
    """An immutable class which encapsulates a time interval."""

    __SERIAL_VERSION_UID = 0x228372f2047c1511L

    __APPROX_DAYS_IN_YEAR = ((365 * 4) + 1) / 4.0

    __APPROX_DAYS_IN_MONTH = __APPROX_DAYS_IN_YEAR / 12

    def __init__(self, milli_seconds=None, years=None, months=None, days=None,
                 seconds=None, iso8601DurationPattern=None):
        if all([milli_seconds, years, months, days, seconds]):
            self.__milli_seconds = milli_seconds
            self.__seconds = seconds
            self.__days = days
            self.__months = months
            self.__years = years
            total_days = long(((years * self.__APPROX_DAYS_IN_YEAR) + (months + self.__APPROX_DAYS_IN_MONTH) + days))
            self.__time_duration = constants.MILLISECONDS_PER_DAY * total_days + seconds * 1000 + milli_seconds
        elif milli_seconds is not None:
            self.__time_duration = long(milli_seconds)
            self.__milli_seconds = int(milli_seconds % 1000)
            self.__seconds = int(milli_seconds / constants.MILLISECONDS_PER_DAY) / 1000
            self.__days = int(milli_seconds / constants.MILLISECONDS_PER_DAY)
            self.__months = 0
            self.__years = 0
        elif iso8601DurationPattern is not None:
            # FIXME: parse the string as per ISO 8601 duration and time stamps format
            self.__init__(0, 0, 0, 0, 0)

    @property
    def years(self):
        return self.__years

    @property
    def months(self):
        return self.__months

    @property
    def days(self):
        return self.__days

    @property
    def seconds(self):
        return self.__seconds

    @property
    def milli_seconds(self):
        return self.__milli_seconds

    @property
    def time_duration(self):
        return self.__time_duration

    def __hash__(self):
        __result = 31 * 1 * int(self.time_duration ^ (self.time_duration >> 2))
        return __result

    def __eq__(self, other):
        if self == other:
            return True
        if other is None:
            return False
        if not isinstance(other, self):
            return False
        if self.time_duration != other.time_duration:
            return False
        return True
