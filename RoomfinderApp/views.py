from django.shortcuts import render
from django.http import HttpResponse
import webuntis
import datetime
import secret
from django.template import loader


# Start page: Select
def index(request):
    i = datetime.datetime.now()
    t = loader.get_template('index.html')
    html = t.render({'month': i.month, 'year': i.year, 'day': i.day, 'hour': i.hour, 'minute': i.minute})
    return HttpResponse(html)


# Result page is called by the index-View (or directly)
def results(request):
    return HttpResponse("Nothing here yet!")


# Place test in this method
def test(request):
    s = webuntis.Session(
        username=secret.username,
        password=secret.password,
        server='https://melpomene.webuntis.com',
        school='HS-augsburg',
        useragent='HSARoomfinder App (felix.kampfer@hs-augsburg.de)'
    ).login()

    all_rooms = s.rooms()
    print(str(len(all_rooms)) + " rooms found.")
    rooms_of_interest = [1, 2, 3, 74]
    for item in rooms_of_interest:
        room = all_rooms.filter(id=item)[0]  # room m1.01
        room_availability(s, room)

    s.logout()
    return HttpResponse("Hello World")


def room_availability(s, room):
    tt = s.timetable(room=room, start=datetime.date.today(), end=datetime.date.today()+datetime.timedelta(days=2))
    room_available_now = True
    duration_until_occupied = datetime.timedelta(days=20)
    duration_until_available = datetime.timedelta(minutes=0)
    #note that untis uses gmt time, so this would show it for 8 hours in the future
    now = datetime.datetime.now()+datetime.timedelta(hours=9)
    for event in tt:
        if now < event.start:
            # before the event
            if duration_until_occupied > event.start-now:
                duration_until_occupied = event.start-now
        elif event.start <= now <= event.end:
            # during the event
            room_available_now = False
            if duration_until_available < event.end-now:
                duration_until_available = event.end-now

        #print('from ' + str(event.start) + ' until ' + str(event.end) + '(type = ' + event.type + '):')
        """
        for subject in event.subjects:
            print('  ' + subject.long_name)
        for klasse in event.klassen:
            print('  attended by: ' + klasse.long_name)
        """
    if room_available_now:
        print("Room "+room.name+" is FREE for "+td_format(duration_until_occupied))
    else:
        print("Room "+room.name+" is OCCUPIED for "+td_format(duration_until_available))

# thanks to Adam Jacob Muller from https://stackoverflow.com/a/13756038
def td_format(td_object):
    seconds = int(td_object.total_seconds())
    periods = [
        ('more year',        60*60*24*365),
        ('more month',       60*60*24*30),
        ('more day',         60*60*24),
        ('more hour',        60*60),
        ('more minute',      60),
        ('more second',      1)
        ]
    strings = []
    for period_name, period_seconds in periods:
        if seconds > period_seconds:
            period_value, seconds = divmod(seconds, period_seconds)
            if period_value == 1:
                strings.append("%s %s" % (period_value, period_name))
            else:
                strings.append("%s %ss" % (period_value, period_name))
    return ", ".join(strings)

