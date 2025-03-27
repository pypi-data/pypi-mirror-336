#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Thu Mar 13 14:32:31 2025

@author: Wiesinger Franz
'''


# Python 3+
import pytz
from datetime import datetime
from zoneinfo import ZoneInfo
import tkinter as tk
from tkinter import messagebox


class DateTimeChecker(datetime):

    def __init__(self):
        super().__init__(self)

    def get_timezonelist():
        tzlist = pytz.all_timezones
        return tzlist

    def get_localtime(zoneinfo):
        loc_time = datetime.now(tzinfo=ZoneInfo(key=zoneinfo))
        return loc_time

    def check_dt_string(dtimestr):
        valid = True
        formatstr = '%Y-%m-%d %H:%M:%S'
        try:
            ts = datetime.strptime(dtimestr, formatstr)
            if ts:
                valid = True
                return valid

        except ValueError:
            valid = False
            return False

    def show_warning(self, exc, msg):
        messagebox.showwarning(exc, msg)

    def local_utc_ux(self, time, tzinfo):
        tz = pytz.timezone(tzinfo)
        formatstr = '%Y-%m-%d %H:%M:%S'
        ts = datetime.strptime(time, formatstr)
        loc_ts = tz.localize(ts)
        time_uc = loc_ts.astimezone(pytz.utc)
        time_ux = int(loc_ts.astimezone(pytz.utc).timestamp())
        insert_utc = datetime.strftime(time_uc, formatstr)
        return insert_utc, time_ux

    def utc_loc_ux(self, time, tzinfo):
        formatstr = '%Y-%m-%d %H:%M:%S'
        tz_loc = pytz.timezone(tzinfo)
        tz_utc = pytz.timezone('UTC')
        utc_form = datetime.strptime(time, formatstr)
        localized_utc = utc_form.replace(tzinfo=tz_utc)
        # convert timestrin from utc to a utc-datetime incl. timezone
        loc_time = localized_utc.astimezone(tz_loc)
        # convert utc into unixtime
        time_ux = int(localized_utc.timestamp())
        ts = datetime.strftime(loc_time, formatstr)
        insert_utc = datetime.strftime(localized_utc, formatstr)
        return insert_utc, time_ux, ts

    def ux_utc_loc(self, time, tzinfo):
        # tz_loc = timezone local
        # tz_utc = timezone utc
        # tutc = time utc
        # ins_utc = insert utc value
        # ins_loc = insert local time value
        tz_loc = pytz.timezone(tzinfo)
        tz_utc = pytz.timezone('UTC')
        tutc = datetime.fromtimestamp(int(time), tz_utc)
        formatstr = '%Y-%m-%d %H:%M:%S'
        ins_utc = datetime.strftime(tutc, formatstr)
        time_loc = datetime.fromtimestamp(int(time), tz_loc)
        ins_loc = datetime.strftime(time_loc, formatstr)
        return ins_utc, int(time), ins_loc


class InpValidator:
    '''Adds validation functionality to entry fields'''

    def __init__(
            self, *args, **kwargs
    ):
        super().__init__(*args, **kwargs)

    def _toggle_error(self, on=False):
        self.configure(foreground=('red' if on else 'black'))

    def val(self, prop, char, event, index, action, framename):

        valid = True
        entryobjname = framename.split('.')[-1]

        if event == 'key' and entryobjname in ('time_loc', 'time_utc'):

            if len(char) > 5:
                dtimestr = char
                valid = DateTimeChecker.check_dt_string(dtimestr)
                if valid is True:
                    return valid
                elif valid is False:
                    return valid

            if action == '0':  # This is a delete action
                valid = True
            elif index in (
                '0', '1', '2', '3', '5', '6', '8', '9', '11', '12', '14', '15',
                '17', '18'
            ):
                valid = char.isdigit()

            elif index in ('4', '7'):
                valid = char == '-'
            elif index == '10':
                valid = char == ' '
            elif index in ('13', '16'):
                valid = char == ':'
            else:
                valid = False

            return valid

        elif event == 'key' and entryobjname == 'time_ux':
            valid = True

            if action == '0':  # This is a delete action
                valid = True
            elif index in (
                '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10'
            ):
                valid = char.isdigit()
            else:
                valid = False
            return valid


class CheckEntryData(DateTimeChecker):
    '''All functions and methods happened at focusout in entry objects'''

    def __init__(
            self, *args, error_var=None, **kwargs
    ):
        self.error = error_var or tk.StringVar()
        super().__init__(*args, **kwargs)

    def check_input_data(self, name):
        valid = True

        if name in ('time_loc', 'time_utc'):
            if name == 'time_loc':
                dtimestr = self.ent_time_loc.get()
            else:
                dtimestr = self.ent_time_utc.get()

            if dtimestr:
                valid = DateTimeChecker.check_dt_string(dtimestr)

                if valid is False:
                    msg = 'Not a valid date time!'
                    exc = 'Warning - Wrong datetime'
                    DateTimeChecker.show_warning(self, exc, msg)
                    valid = False
                    return

            formatstr = '%Y-%m-%d %H:%M:%S'
            vtimestamp = int(
                datetime.strptime(dtimestr, formatstr).timestamp()
            )

            if vtimestamp < 1:
                msg = (
                    'No valid unixtime! \n'
                    + 'Date and time before 1970-01-01 14:00:00! \n'
                    + 'this is before the Unix epoch!'
                    + 'the lowest value for converting is 1'
                )
                exc = 'Warning - Wrong Unixtime'
                DateTimeChecker.show_warning('', exc, msg)
                valid = False
                return

            elif vtimestamp > 99999999999:
                msg = (
                    'No valid unixtime! \n'
                    + 'Date and time after  5138-11-16 09:46:39! \n'
                    + 'We do not convert time after this date and time!'
                )
                exc = 'Warning - Wrong Unixtime'
                DateTimeChecker.show_warning(self, exc, msg)
                valid = False
                return

        elif name == 'time_ux':
            vux = int(self.ent_time_ux.get())

            if vux > 99999999999:
                msg = (
                    'No valid unixtime!\n' +
                    'The max value = 99999999999!'
                )
                exc = 'Warning - Invalid Unixtime'
                DateTimeChecker.show_warning(self, exc, msg)
                valid = False
                return

            if vux < 1:
                msg = (
                    'No valid unixtime!\n' +
                    'The min value = 1!'
                )
                exc = 'Warning - Invalid Unixtime'
                DateTimeChecker.show_warning(self, exc, msg)
                valid = False
                return

        return valid

    def reset_time_entries(self):
        t_loc = self.ent_time_loc
        t_utc = self.ent_time_utc
        t_ux = self.ent_time_ux

        timefields = [t_loc, t_utc, t_ux]

        for field in timefields:
            try:
                entryvalue = field.get()
                if not entryvalue:
                    pass
                else:
                    field.delete(0, tk.END)
            except Exception:
                msg = 'An error at the resetoperation happened'
                exc = 'Warning - reset error'
                DateTimeChecker.show_warning(self, exc, msg)
