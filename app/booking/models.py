from django.contrib.auth import get_user_model
from django.db import models


class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    booker = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)  # who's reserve this

    def __str__(self):
        return f"{self.booker.username} reserve {self.first_name} {self.last_name}"


class Table(models.Model):
    seats = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.seats} seats"


class Seat(models.Model):
    table = models.ForeignKey(Table, on_delete=models.CASCADE)
    cost = models.PositiveIntegerField()
    is_reserved = models.BooleanField(default=False)

    def __str__(self):
        return f"seat {self.id} for table {self.table} with cost {self.cost}"


class Booking(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    seat = models.ForeignKey(Seat, on_delete=models.CASCADE)
    is_cancelled = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.seat.id} reserve for person with id {self.person.id}"
