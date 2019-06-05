#!/usr/bin/env python
import sys
import codecs
import time
import re
from datetime  import timedelta, datetime, tzinfo
from icalendar import Calendar, Event, vDatetime

class SystemTimeZone(tzinfo):
    def utcoffset(self, dt):
        offset = time.timezone if (time.localtime().tm_isdst == 0) else time.altzone
        offset *= -1
        return timedelta(seconds=offset)

    def dst(self, dt):
        offset = 0 if (time.localtime().tm_isdst == 0) else time.timezone - time.altzone
        offset *= -1
        return timedelta(seconds=offset)

    def tzname(self, dt):
        return time.tzname[0]

sys.stdout = codecs.getwriter('utf8')(sys.stdout)

def parse_contact(contact):
    cn = contact.params['cn'] \
         + '  <' + re.sub('MAILTO:', '', contact) + '>'
    return cn

cal = Calendar.from_ical(sys.stdin.read().decode('utf-8'))

for event in cal.walk('vevent'):
    systemTZ = SystemTimeZone()
    print "Event:    ", event['summary']
    print "Location: ", event['location']
    print ""
    print "Organizer: ", parse_contact(event['organizer'])
    print ""
    print "Start:     ", event['dtstart'].dt.isoformat(' ') \
        + '  ' + event['dtstart'].params['tzid']
    print "     local:", event['dtstart'].dt.astimezone(systemTZ)
    print "Stop:      ", event['dtend'].dt.isoformat(' ') \
        + '  ' + event['dtend'].params['tzid']
    print "     local:", event['dtend'].dt.astimezone(systemTZ)
    print ""
    try:
        print event['description']
    except KeyError:
        print "(description not set)"
    print ""
    print "Attenders: ", len(event['attendee'])
    for attendee in event['attendee']:
        print "    ", parse_contact(attendee)


