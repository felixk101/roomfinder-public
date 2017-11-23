from django.shortcuts import render
from django.http import HttpResponse
import webuntis
import datetime
import secret
from django.core import serializers
from django.template import loader
from django.shortcuts import render
from RoomfinderApp.models import Building,Room,Event

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
            room_info = get_room_info(bdaytime, buildings, levels)
            json_data = convert_to_json(room_info)
            return render(request, 'result.html', {"json_data": json_data})
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
    update_database()
    return HttpResponse("Done updating")

def get_room_info(bdaytime, buildings, floors):
    #jedes Gebäude ist jetzt ein einzelner Eintrag
    if 'KLM' in buildings:
        buildings.remove('KLM')
        buildings.append('K')
        buildings.append('L')
        buildings.append('M')
    #wir unteressieren uns nur für "2", nicht "level 2"
    floors = [floor[-1] for floor in floors]

    s = webuntis.Session(
        username=secret.username,
        password=secret.password,
        server='https://melpomene.webuntis.com',
        school='HS-augsburg',
        useragent='HSARoomfinder App (felix.kampfer@hs-augsburg.de)'
    ).login()
    all_rooms = s.rooms()
    # wir wollen nur die Räume in den ausgewaehlten Gebäuden in den jeweiligen Stockwerken (anhand des Namens)
    requested_rooms = filter(lambda room: room.name[0] in buildings and room.name[1] in floors, all_rooms)
    room_info = []
    print(requested_rooms)
    for room in requested_rooms:
        availability, time_until_change = room_availability(s, room, bdaytime)
        room_info.append(Room(room.name, availability, time_until_change))
        pass
    s.logout()
    return room_info



def room_availability(s, room, bdaytime):
    try:
        requested_time = datetime.datetime.strptime(bdaytime, '%Y-%m-%dT%H:%M:%S')
    except ValueError:
        requested_time = datetime.datetime.strptime(bdaytime, '%Y-%m-%dT%H:%M')
    tt = s.timetable(room=room, start=requested_time, end=requested_time+datetime.timedelta(days=2))
    room_available_now = True
    duration_until_occupied = datetime.timedelta(days=20)
    duration_until_available = datetime.timedelta(minutes=0)
    #note that untis uses gmt time, so this would show it for 8 hours in the future
    #now = datetime.datetime.now()+datetime.timedelta(hours=9)
    now = requested_time
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
        return room_available_now, td_format(duration_until_occupied)
    else:
        print("Room "+room.name+" is OCCUPIED for "+td_format(duration_until_available))
        return room_available_now, td_format(duration_until_available)


def convert_to_json(room_info):
    my_string = "["
    for room in room_info:
        my_string += '{ ' \
                     '\"name\":\"' + room.name + '\", ' \
                     '\"free\":'+str(room.free).lower()+', ' \
                     '\"duration_until_change\":\"'+room.duration_until_change+'\"' \
                     '},'
    my_string = my_string[:-1]
    my_string += "]"
    return my_string


def update_database():
    s = webuntis.Session(
        username=secret.username,
        password=secret.password,
        server='https://melpomene.webuntis.com',
        school='HS-augsburg',
        useragent='HSARoomfinder App (felix.kampfer@hs-augsburg.de)'
    ).login()

    # reset table
    Building.objects.all().delete()

    # insert buildings in database
    brunnenlech_buildings = ["A", "B", "C", "D", "E", "F", "G", "H", "N", "R"]
    for building_name in brunnenlech_buildings:
        building = Building(campus="brunnenlech",name=building_name)
        building.save()
    rotes_tor_buildings = ["K", "L", "M", "J", "W"]
    for building_name in rotes_tor_buildings:
        building = Building(campus="rotes_tor", name=building_name)
        building.save()

    # insert rooms in database
    all_untis_rooms = s.rooms()
    print("Inserting "+str(len(all_untis_rooms)) + " rooms.")
    for index, untis_room in enumerate(all_untis_rooms):
        print("handling room "+untis_room.name)
        # handle special cases
        if Room.objects.all().filter(name=untis_room.name).exists():
            print("ignoring DUPLICATE room " + untis_room.name)
            continue
        if not untis_room.name[0] in brunnenlech_buildings + rotes_tor_buildings:
            print("ignoring room " + untis_room.name + " in a building that doesn't exist")
            continue
        if not untis_room.name[1].isdigit():
            print("ignoring weirdly-named room " + untis_room.name)
            continue

        room = Room(name=untis_room.name,
                    long_name=untis_room.long_name,
                    building=Building.objects.get(name=untis_room.name[0]),
                    floor=int(untis_room.name[1])
                    )
        room.save()
        # insert events in database
        untis_events = s.timetable(room=untis_room,start=datetime.datetime.now(),end=(datetime.datetime.now()+datetime.timedelta(days=7)))
        for untis_event in untis_events:
            subject = untis_event.subjects[0].name if len(untis_event.subjects) > 0 else "Unnamed Subject"
            event = Event(start=untis_event.start,
                          end=untis_event.end,
                          room=Room.objects.get(name=untis_room.name),
                          subject=subject
                          )
            event.save()
        print("Inserted room "+untis_room.name+" with "+str(len(untis_events)) + " events. ("+str(index)+"/"+str(len(all_untis_rooms))+")")
    s.logout()


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

"""
class Room:

    def __init__(self, name, free, duration_until_change):
        self.name = name
        self.free = free
        self.duration_until_change = duration_until_change


class Building:
    rooms = []

    def __init__(self, name):
        self.name = name
"""
