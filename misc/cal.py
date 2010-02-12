"""
Gregorian Calendar

This module demostrate the calculation of Gregorian Calendar with Zeller's Rule
Details please see http://www.geocities.com/calshing/dayofweek.htm
"""
__author__ = "Jiang Yu-Kuan, yukuan.jiang(at)gmail.com"
__date__ = "2008/08/23 (initial version)"
__version__ = "1.5"


def weekHeader():
    return "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"


def isLeap(year):
    """Decide whether a given year is a leap year.

    Example
    -------
    >>> isLeap(1995)
    False
    >>> isLeap(2004)
    True
    """
    return (year%4 == 0 and year%100 != 0) or (year%400 == 0)


def daysOfMonth(year, month):
    """Return the total days for year (1584-...), month (1-12).

    Example
    -------
    >>> daysOfMonth(1995, 2)
    28
    >>> daysOfMonth(2008, 3)
    31
    """
    d = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if isLeap(year):
        d[1] += 1
    return d[month-1]


def Zeller(year, month, day):
    """Use Zeller's formula to calculate the day (0-6; 0 is Sunday)
    of the week of a given date.

    Example
    -------
    >>> Zeller(2009, 3, 7)
    6
    """
    a = (14 - month) / 12
    C = year/100
    Y = year%100 - a
    M = month + 12*a - 2
    D = day
    return (C/4 - 2*C + Y + Y/4 + (13*M-1)/5 + D) % 7


def Zeller_m(year, month, day):
    """Use a modified Zeller's formula to calculate the day (0-6; 0 is Sunday)
    of the week of a given date.

    Example
    -------
    >>> Zeller_m(2009, 2, 22)
    0
    """
    a = (14-month)/12
    Y = year - a
    M = month + 12*a - 2
    D = day
    return (Y + Y/4 - Y/100 + Y/400 + 31*M/12 + D) % 7


def weekday(year, month, day):
    """Return the day (0-6; 0 is Sunday) of the week for year (1584-...),
    month (1-12), day (1-31).

    Example
    -------
    >>> weekday(2009, 3, 7)
    6
    """
    return Zeller_m(year, month, day)


def firstWeekdayOfMonth(year, month):
    """Return the day (0-6; 0 is Sunday) of the week for the first day
    of a month with a given year (1584-...) and month (1-12).

    Example
    -------
    >>> firstWeekdayOfMonth(2009, 3)
    0
    """
    return weekday(year, month, 1)


def AMPM_from_military(h):
    """Return an AM/PM hour from its 24-hour (military time) version.
    ref. http://www.onlineconversion.com/date_12-24_hour.htm

    Example
    -------
    >>> militaries = [12,] + range(1, 12)
    >>> militaries
    [12, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    >>> [AMPM_from_military(h) for h in range(24)] == militaries*2
    True
    """
    h %= 12
    if (h == 0):
        h = 12
    return h


def military_from_AMPM(h, ampm):
    """Return a military hour (0-23) from its 12-hour AM/PM version.
    ref. http://www.onlineconversion.com/date_12-24_hour.htm

    Arguments
    ---------
    h: an AM/PM hour
    ampm: 0 means AM; 1 means PM

    Example
    -------
    >>> hours = [AMPM_from_military(h) for h in range(24)]
    >>> AM, PM = 0, 1
    >>> ampms = [AM,]*12 + [PM,]*12
    >>> [military_from_AMPM(h, a) for h, a in zip(hours, ampms)] == range(24)
    True
    """
    if (h == 12):
        h = 0
    return h + ampm*12


if __name__ == "__main__":
    import doctest
    doctest.testmod()
