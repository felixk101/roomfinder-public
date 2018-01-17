from django.shortcuts import render
from django.http import HttpResponse
import webuntis
import datetime
import pytz
import secret
from django.core import serializers
from django.template import loader
from RoomfinderApp.models import Building, Room, Event


# Start page: Select
def index(request):
    return render(request, 'index.html')


def update(request):
    update_database()
    return HttpResponse("Done updating")


def result(request, building):
    buildings = [building]
    db_room = Building.objects.get(name=building)
    floors = set([room.floor for room in Room.objects.all().filter(building=db_room)])

    if "K" in buildings or "L" in buildings or "M" in buildings:
        buildings.append("K")
        buildings.append("L")
        buildings.append("M")
        buildings = list(set(buildings))
    room_info = get_room_info(datetime.datetime.now(), buildings, floors)
    json_data = convert_to_json(room_info)
    return render(request, 'result.html', {"buildings": buildings, "floors": floors, "room_info": room_info, "json_data": json_data})


def get_room_info(daytime, buildings, floors):
    room_info = []
    for room in Room.objects.filter(building__in=Building.objects.filter(name__in=buildings), floor__in=floors):
        # availability = not Event.objects.filter(room=room, start__lt=bdaytime, end__gt=bdaytime).exists()
        availability = True
        duration_until_occupied = datetime.timedelta(days=20)
        duration_until_available = datetime.timedelta(minutes=0)

        """
        if available:
            find shortest duration_until_occupied
                find minimum (event.start- now) where (event.start - now) > 0
        else
            find shortest duration_until_free:
                find minimum (event.end - now) where (event.end - now) > 0
            
        """
        timezone = pytz.timezone('Europe/Berlin')
        now = timezone.localize(daytime)
        for event in Event.objects.filter(room=room):
            if now < event.start:
                # before the event
                if duration_until_occupied > event.start - now:
                    duration_until_occupied = event.start - now
            elif event.start <= now <= event.end:
                # during the event
                availability = False
                if duration_until_available < event.end - now:
                    duration_until_available = event.end - now
        time_until_change = (duration_until_occupied if availability else duration_until_available)
        room_info.append(RoomView(room.name, availability, time_until_change))
    if "K" in buildings:
        buildings.remove("K")
        buildings.remove("L")
        buildings.remove("M")
        buildings.append("KLM")
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
                     '\"duration_until_change\":\"'+str(room.duration_until_change)+'\"' \
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

    # insert buildings into database
    brunnenlech_buildings = ["A", "B", "C", "D", "E", "F", "G", "H", "N", "R"]
    for building_name in brunnenlech_buildings:
        building = Building(campus="brunnenlech",name=building_name)
        building.save()
    rotes_tor_buildings = ["K", "L", "M", "J", "W"]
    for building_name in rotes_tor_buildings:
        building = Building(campus="rotes_tor", name=building_name)
        building.save()

    # insert rooms into database
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
            timezone = pytz.timezone('Europe/Berlin')
            event = Event(start=timezone.localize(untis_event.start),
                          end=timezone.localize(untis_event.end),
                          room=Room.objects.get(name=untis_room.name),
                          subject=subject
                          )
            event.save()
        print("Inserted room "+untis_room.name+" with "+str(len(untis_events)) + " events. ("+str(index+1)+"/"+str(len(all_untis_rooms))+")")
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


class RoomView:
    def __init__(self, name, free, duration_until_change):
        self.name = name
        self.free = free
        self.duration_until_change = duration_until_change
