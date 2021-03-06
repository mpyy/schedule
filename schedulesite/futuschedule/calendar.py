import datetime
from futuschedule import util


def createEvent(calendarId, sendNotifications, summary, description, location,
        startDt, endDt, tzName, attendingEmails):
    """
    Create a new calendar event and return it.

    TODO: use some docstring format for function params.
    start/end - datetime.datetime objects in local time (.tzinfo is ignored)
    tzName - the timezone for the local times in start&end

    We let Google Calendar handle timezones, and when DST switches occur.
    Alternatively we can use pytz.localize(naive_datetime).isoformat() and pass
    only the 'dateTime' field to Google (in format '...+03:00'),
    without the 'timezone' field.
    """

    def getNaive(dt):
        """Return a naive datetime object for a possibly tz-aware one."""
        return datetime.datetime(dt.year, dt.month, dt.day, dt.hour, dt.minute)

    startDt, endDt = map(getNaive, (startDt, endDt))

    event = {
            'summary': summary,
            'description': description,
            'location': location,
            'start': {
                'dateTime': startDt.isoformat(),
                'timeZone': tzName,
            },
            'end': {
                'dateTime': endDt.isoformat(),
                'timeZone': tzName,
            },
            'attendees': map(lambda x: {'email': x}, attendingEmails),
    }
    calSvc = util.buildCalendarSvc()
    return calSvc.events().insert(calendarId=calendarId,
            sendNotifications=sendNotifications, body=event).execute()


def deleteEvent(calendarId, eventId, sendNotifications=False):
    """
    Delete the calendar event.
    """
    calSvc = util.buildCalendarSvc()
    calSvc.events().delete(calendarId=calendarId, eventId=eventId,
            sendNotifications=sendNotifications).execute()
