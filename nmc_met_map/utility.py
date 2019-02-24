# _*_ coding: utf-8 _*_

"""
  Some utility funcations.
"""

from datetime import datetime


def model_filename(initial_time, fhour):
    """
        Construct model file name.

    Arguments:
        initial_time {string or datetime object} -- model initial time,
            like 18042008' or datetime(2018, 4, 20, 8).
        fhour {int} -- model forecast hours.
    """

    if isinstance(initial_time, datetime):
        return initial_time.strftime('%y%m%d%H') + ".{:03d}".format(fhour)
    else:
        return initial_time.strip() + ".{:03d}".format(fhour)
