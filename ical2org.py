#!/usr/bin/env python
import sys, os
import codecs

from icalendar import Calendar, Event, vDatetime
from datetime  import timedelta, datetime, tzinfo

class GmtMinus5(tzinfo):
    def utcoffset(self, dt):
        return timedelta(hours=-5) + self.dst(dt)

    def dst(self, dt):
        return timedelta(0)

    def tzname(self, dt):
        return "GMT -5"

org_file = os.path.join(os.path.expanduser("~"), "Documents/org/meetings.org")

def toOrgMode(start, stop):
    gmtMinus5 = GmtMinus5()
    dts = start.dt.astimezone(gmtMinus5)
    dte = stop.dt.astimezone(gmtMinus5)
    str = dts.strftime('<%Y-%m-%d %a %H:%M>')
    str += "--"
    str += dte.strftime('<%Y-%m-%d %a %H:%M>')
    return str

f = open(sys.argv[1], 'rb')

try:
    cal = Calendar.from_ical(f.read())
except ValueError:
    print "Not a valid ical file!"
    sys.exit(1)

gmtMinus5 = GmtMinus5()

for event in cal.walk('vevent'):
    print "Event:    ", event['summary']
    print "Location: ", event['location']
    print "From:     ", event.decoded('dtstart').astimezone(gmtMinus5)
    print "To:       ", event.decoded('dtend').astimezone(gmtMinus5)
    print ""
    confirmation = raw_input("Add to calendar? ")
    if ((confirmation.lower() == 'yes') or (confirmation.lower() == 'y')):
        outfile = codecs.open(org_file, 'a+b', 'utf-8')
        print "Output file: ", outfile
        outfile.write("* " + event['summary'] + "\n")
        outfile.write(toOrgMode(event['dtstart'], event['dtend']) + "\n")
        outfile.write(event['location'] + "\n")
        try:
            outfile.write(event['description'] + "\n")
        except KeyError:
            outfile.write("(description not set)\n")
        outfile.write("\n")
        outfile.close()

