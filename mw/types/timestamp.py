import calendar
import datetime
import time

from . import serializable

LONG_MW_TIME_STRING = '%Y-%m-%dT%H:%M:%SZ'
"""
The longhand version of MediaWiki time strings.
"""

SHORT_MW_TIME_STRING = '%Y%m%d%H%M%S'
"""
The shorthand version of MediaWiki time strings.
"""


class Timestamp(serializable.Type):
    """
    An immutable type for working with MediaWiki timestamps in their various
    forms.

    :Parameters:
        time_thing : :class:`mw.Timestamp` | :py:class:`~time.time_struct` | :py:class:`~datetime.datetime` | :py:class:`str` | :py:class:`int` | :py:class:`float`
            The timestamp type from which to construct the timestamp class.

    :Returns:
        :class:`mw.Timestamp`

    You can make use of a lot of different *time things* to initialize a
    :class:`mw.Timestamp`.

    * If a :py:class:`~time.time_struct` or :py:class:`~datetime.datetime` are provided, a `Timestamp` will be constructed from their values.
    * If an `int` or `float` are provided, they will be assumed to a unix timestamp in seconds since Jan. 1st, 1970 UTC.
    * If a `str` is provided, it will be be checked against known MediaWiki timestamp formats.  E.g., ``'%Y%m%d%H%M%S'`` and ``'%Y-%m-%dT%H:%M:%SZ'``.
    * If a :class:`mw.Timestamp` is provided, the same `Timestamp` will be returned.

    For example::

        >>> import datetime, time
        >>> from mw import Timestamp
        >>> Timestamp(1234567890)
        Timestamp('2009-02-13T23:31:30Z')
        >>> Timestamp(1234567890) == Timestamp("2009-02-13T23:31:30Z")
        True
        >>> Timestamp(1234567890) == Timestamp("20090213233130")
        True
        >>> Timestamp(1234567890) == Timestamp(datetime.datetime.utcfromtimestamp(1234567890))
        True
        >>> Timestamp(1234567890) == Timestamp(time.strptime("2009-02-13T23:31:30Z", "%Y-%m-%dT%H:%M:%SZ"))
        True
        >>> Timestamp(1234567890) == Timestamp(Timestamp(1234567890))
        True


    You can also do math and comparisons of timestamps.::

        >>> from mw import Timestamp
        >>> t = Timestamp(1234567890)
        >>> t
        Timestamp('2009-02-13T23:31:30Z')
        >>> t2 = t + 10
        >>> t2
        Timestamp('2009-02-13T23:31:40Z')
        >>> t += 1
        >>> t
        Timestamp('2009-02-13T23:31:31Z')
        >>> t2 - t
        9
        >>> t < t2
        True


    """

    def __new__(cls, time_thing):
        if isinstance(time_thing, cls):
            return time_thing
        elif isinstance(time_thing, time.struct_time):
            return cls.from_time_struct(time_thing)
        elif isinstance(time_thing, datetime.datetime):
            return cls.from_datetime(time_thing)
        elif type(time_thing) in (int, float):
            return cls.from_unix(time_thing)
        else:
            return cls.from_string(time_thing)

    def __init__(self, time_thing):
        # Important that this does nothing in order to allow __new__ to behave
        # as expected.  User `initialize()` instead.
        pass

    def initialize(self, time_struct):
        self.__time = time_struct

    def short_format(self):
        """
        Constructs a long, ``'%Y%m%d%H%M%S'`` formatted string common to the
        database. This method is roughly equivalent to calling
        ``strftime('%Y%m%d%H%M%S')``.

        :Parameters:
            format : str
                The string format

        :Returns:
            A formatted string
        """
        return self.strftime(SHORT_MW_TIME_STRING)

    def long_format(self):
        """
        Constructs a long, ``'%Y-%m-%dT%H:%M:%SZ'`` formatted string common to the
        API. This method is roughly equivalent to calling
        ``strftime('%Y-%m-%dT%H:%M:%SZ')``.

        :Parameters:
            format : str
                The string format

        :Returns:
            A formatted string
        """
        return self.strftime(LONG_MW_TIME_STRING)

    def strftime(self, format):
        """
        Constructs a formatted string.
        See `<https://docs.python.org/3/library/time.html#time.strftime>`_ for a
        discussion of formats descriptors.

        :Parameters:
            format : str
                The format description

        :Returns:
            A formatted string
        """
        return time.strftime(format, self.__time)

    @classmethod
    def strptime(cls, string, format):
        """
        Constructs a :class:`mw.Timestamp` from an explicitly formatted string.
        See `<https://docs.python.org/3/library/time.html#time.strftime>`_ for a
        discussion of formats descriptors.

        :Parameters:
            string : str
                A formatted timestamp
            format : str
                The format description

        :Returns:
            :class:`mw.Timestamp`
        """
        return cls.from_time_struct(time.strptime(string, format))

    @classmethod
    def from_time_struct(cls, time_struct):
        """
        Constructs a :class:`mw.Timestamp` from a :class:`time.time_struct`.

        :Parameters:
            time_struct : :class:`time.time_struct`
                A time structure

        :Returns:
            :class:`mw.Timestamp`
        """
        instance = super().__new__(cls)
        instance.initialize(time_struct)
        return instance

    @classmethod
    def from_datetime(cls, dt):
        """
        Constructs a :class:`mw.Timestamp` from a :class:`datetime.datetime`.

        :Parameters:
            dt : :class:`datetime.datetime``
                A datetime.

        :Returns:
            :class:`mw.Timestamp`
        """
        time_struct = dt.timetuple()
        return cls.from_time_struct(time_struct)

    @classmethod
    def from_unix(cls, seconds):
        """
        Constructs a :class:`mw.Timestamp` from a unix timestamp (in seconds
        since Jan. 1st, 1970 UTC).

        :Parameters:
            seconds : int
                A unix timestamp

        :Returns:
            :class:`mw.Timestamp`
        """
        time_struct = datetime.datetime.utcfromtimestamp(seconds).timetuple()
        return cls.from_time_struct(time_struct)

    @classmethod
    def from_string(cls, string):
        """
        Constructs a :class:`mw.Timestamp` from a MediaWiki formatted string.
        This method is provides a convenient way to construct from common
        MediaWiki timestamp formats. E.g., ``%Y%m%d%H%M%S`` and
        ``%Y-%m-%dT%H:%M:%SZ``.

        :Parameters:
            string : str
                A formatted timestamp

        :Returns:
            :class:`mw.Timestamp`
        """
        if type(string) == bytes:
            string = str(string, 'utf8')
        else:
            string = str(string)

        try:
            return cls.strptime(string, SHORT_MW_TIME_STRING)
        except ValueError as e:
            try:
                return cls.strptime(string, LONG_MW_TIME_STRING)
            except ValueError as e:
                raise ValueError(
                    "{0} is not a valid Wikipedia date format".format(
                        repr(string)
                    )
                )

        return cls.from_time_struct(time_struct)

    def __format__(self, format):
        return self.strftime(format)

    def __str__(self):
        return self.short_format()

    def serialize(self):
        return self.unix()

    @classmethod
    def deserialize(cls, time_thing):
        return Timestamp(time_thing)

    def __repr__(self):
        return "{0}({1})".format(
            self.__class__.__name__,
            repr(self.long_format())
        )

    def __int__(self):
        return self.unix()

    def __float__(self):
        return float(self.unix())

    def unix(self):
        """
        :Returns:
            the number of seconds since Jan. 1st, 1970 UTC.
        """
        return int(calendar.timegm(self.__time))

    def __sub__(self, other):
        if isinstance(other, Timestamp):
            return self.unix() - other.unix()
        else:
            return self + (other * -1)

    def __add__(self, seconds):
        return Timestamp(self.unix() + seconds)

    def __eq__(self, other):
        try:
            return self.__time == other.__time
        except AttributeError:
            return False

    def __lt__(self, other):
        try:
            return self.__time < other.__time
        except AttributeError:
            return NotImplemented

    def __gt__(self, other):
        try:
            return self.__time > other.__time
        except AttributeError:
            return NotImplemented

    def __le__(self, other):
        try:
            return self.__time <= other.__time
        except AttributeError:
            return NotImplemented

    def __ge__(self, other):
        try:
            return self.__time >= other.__time
        except AttributeError:
            return NotImplemented

    def __ne__(self, other):
        try:
            return not self.__time == other.__time
        except AttributeError:
            return NotImplemented
        
    def __getnewargs__(self):
        return (self.__time,)
