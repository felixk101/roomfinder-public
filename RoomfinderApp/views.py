from django.shortcuts import render
from django.http import HttpResponse
import webuntis
import datetime
import secret
from django.template import loader
from django.shortcuts import render

# TODO: Anderer Hintergrund notwendig!

# Function getselectedbuildings()
# returns True if buildings where found otherwise False
# parameter: request object, buildings: list of buildings (returned)
def getselectedbuildings(request, buildings):
    returnvalue = False
    if 'A' in request.GET:
        gebaeude = request.GET['A']
        if gebaeude:
            returnvalue = True
            buildings.append('A')
    if 'B' in request.GET:
        gebaeude = request.GET['B']
        if gebaeude:
            returnvalue = True
            buildings.append('B')
    if 'C' in request.GET:
        gebaeude = request.GET['C']
        if gebaeude:
            returnvalue = True
            buildings.append('C')
    if 'D' in request.GET:
        gebaeude = request.GET['D']
        if gebaeude:
            returnvalue = True
            buildings.append('D')
    if 'E' in request.GET:
        gebaeude = request.GET['E']
        if gebaeude:
            returnvalue = True
            buildings.append('E')
    if 'F' in request.GET:
        gebaeude = request.GET['F']
        if gebaeude:
            returnvalue = True
            buildings.append('F')
    if 'G' in request.GET:
        gebaeude = request.GET['G']
        if gebaeude:
            returnvalue = True
            buildings.append('G')
    if 'H' in request.GET:
        gebaeude = request.GET['H']
        if gebaeude:
            returnvalue = True
            buildings.append('H')
    if 'J' in request.GET:
        gebaeude = request.GET['J']
        if gebaeude:
            returnvalue = True
            buildings.append('J')
    if 'KLM' in request.GET:
        gebaeude = request.GET['KLM']
        if gebaeude:
            returnvalue = True
            buildings.append('KLM')
    if 'N' in request.GET:
        gebaeude = request.GET['N']
        if gebaeude:
            returnvalue = True
            buildings.append('N')
    if 'P' in request.GET:
        gebaeude = request.GET['P']
        if gebaeude:
            returnvalue = True
            buildings.append('P')
    if 'R' in request.GET:
        gebaeude = request.GET['R']
        if gebaeude:
            returnvalue = True
            buildings.append('R')
    if 'W' in request.GET:
        gebaeude = request.GET['W']
        if gebaeude:
            returnvalue = True
            buildings.append('W')
    return returnvalue


# Function getselectedlevels()
# returns True if levels where found otherwise False
# parameter: request object, levels: list of levels (returned)
def getselectedlevels(request, levels):
    returnvalue = False

    if 'level1' in request.GET:
        level = request.GET['level1']
        if level:
            returnvalue = True
            levels.append('level1')
    if 'level2' in request.GET:
        level = request.GET['level2']
        if level:
            returnvalue = True
            levels.append('level2')
    if 'level3' in request.GET:
        level = request.GET['level3']
        if level:
            returnvalue = True
            levels.append('level3')
    if 'level4' in request.GET:
        level = request.GET['level4']
        if level:
            returnvalue = True
            levels.append('level4')

    return returnvalue


# Start page: Select
def index(request):
    if 'bdaytime' in request.GET:
        bdaytime = request.GET['bdaytime']
        wrongdatetime = False

        if not bdaytime:
            wrongdatetime = True

        buildings = []
        nobuilding = not getselectedbuildings(request, buildings)

        levels = []
        nolevel = not getselectedlevels(request, levels)
        if wrongdatetime is False and nobuilding is False and nolevel is False:
            return render(request, 'result.html', {})
        else:
            i = datetime.datetime.now()
            return render(request, 'index.html', {'wrongDateTime': wrongdatetime, 'noBuilding': nobuilding,
                                                  'noLevel': nolevel, 'month': i.month, 'year': i.year,
                                                  'day': i.day, 'hour': i.hour, 'minute': i.minute,
                                                  'levels': levels, 'buildings': buildings})

    else:  # index view no request object available
        i = datetime.datetime.now()
        return render(request, 'index.html', {'month': i.month, 'year': i.year,
                                              'day': i.day, 'hour': i.hour, 'minute': i.minute})





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

