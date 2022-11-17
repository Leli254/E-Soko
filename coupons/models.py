from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone


class Coupon(models.Model):
    coupon_code = models.CharField(max_length=50, unique=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    value=models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    num_available = models.IntegerField(default=1)
    num_used = models.IntegerField(default=0)

    def __str__(self):
        return self.coupon_code
    

    def can_use(self):
        is_active = True

        if self.num_available <= self.num_used:
            is_active = False

        if self.valid_from > timezone.now():
            is_active = False

        if self.valid_to < timezone.now():
            is_active = False

        if self.is_active == False:
            is_active = False

        if self.num_used >= self.num_available and self.num_available != 0:
            is_active = False

        return is_active

    def use(self):
        self.num_used = self.num_used + 1
        if self.num_used >= self.num_available and self.num_available != 0:
            self.is_active = False
        self.save()
