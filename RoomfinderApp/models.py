from django.db import models


class Building(models.Model):
    CAMPUS_CHOICES = (
        ("brunnenlech", "Campus am Brunnenlech"),
        ("rotes_tor", "Campus am Roten Tor")
    )
    campus = models.CharField(
        max_length=100,
        choices=CAMPUS_CHOICES,
        default="rotes_tor"
    )
    name = models.CharField(max_length=1)

    def __str__(self):
        return "Gebäude %s" % self.name


class Room(models.Model):
    name = models.CharField(max_length=10)
    long_name = models.CharField(max_length=200)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    floor = models.IntegerField()

    def __str__(self):
        return "Raum %s" % self.name


class Event(models.Model):
    start = models.DateTimeField()
    end = models.DateTimeField()
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)

    def __str__(self):
        return "Veranstaltung von "+self.start+" bis "+self.end+" in "+self.room


