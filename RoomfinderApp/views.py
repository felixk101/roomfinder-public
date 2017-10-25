from django.shortcuts import render
from django.http import HttpResponse
import webuntis
import datetime
import secret


# Create your views here.
def index(request):
    s = webuntis.Session(
        username=secret.username,
        password=secret.password,
        server='https://melpomene.webuntis.com',
        school='HS-augsburg',
        useragent='HSARoomfinder App (felix.kampfer@hs-augsburg.de)'
    ).login()

    today = datetime.date.today()
    thursday = today - datetime.timedelta(days=today.weekday())
    print(str(datetime.timedelta(days=today.weekday())))
    monday = thursday + datetime.timedelta(days=4)

    room = s.rooms().filter(id=74)[0]  # room m1.01
    tt = s.timetable(room=room, start=monday, end=monday)
    for row in tt:
        print('from ' + str(row.start) + ' until '+str(row.end) + '(type = '+row.type+'):')
        for subject in row.subjects:
            print('  '+subject.long_name)
        for klasse in row.klassen:
            print('  attended by: '+klasse.long_name)
    s.logout()
    return HttpResponse("Hello World")