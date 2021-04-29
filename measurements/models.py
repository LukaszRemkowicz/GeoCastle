from django.conf import settings
from django.db import models

# Create your models here.

STATE = (('Been', 'Been'), ('Wishlist', 'Wishlist'), ('Nope', 'Nope'))


class Locations(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    review = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=120, choices=STATE)
    ide = models.IntegerField()
    # distance = models.DecimalField(max_digits=10, decimal_places=2)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
