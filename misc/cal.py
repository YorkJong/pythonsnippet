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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
