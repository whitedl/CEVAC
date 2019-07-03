"""Handle time functions for sql-python interactions."""

from dateutil import tz
import datetime


def sql_time_str(t):
    """Return time in sql format."""
    return t.strftime('%Y-%m-%d %H:%M:%S')


def time_of_sql(time_str):
    """Return datetime object of time string."""
    t = datetime.datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S.%f')
    return t


def est_to_utc(t):
    """Convert est to utc."""
    from_zone = tz.gettz('America/New_York')
    to_zone = tz.gettz('UTC')

    est = t.replace(tzinfo=from_zone)
    utc = est.astimezone(to_zone)
    return utc


def utc_to_est(t):
    """Convert utc to est."""
    from_zone = tz.gettz('UTC')
    to_zone = tz.gettz('America/New_York')

    utc = t.replace(tzinfo=from_zone)
    est = utc.astimezone(to_zone)
    return est


'''
        /##.*/
       /#%&&%#/
      ./%%%&%%#
      %%%%&%&%%#
     %&&  %%%&%%.
     %&%  &%%&%%*
     *%&@&@%&%%(
       %%%%%%%%
'''
