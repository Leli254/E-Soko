import uuid
from django.db import models


class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# M-pesa Payment models

class MpesaCalls(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = 'Mpesa Call'
        verbose_name_plural = 'Mpesa Calls'


class MpesaCallBacks(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = 'Mpesa Call Back'
        verbose_name_plural = 'Mpesa Call Backs'


class MpesaPayment(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    type = models.TextField()
    reference = models.TextField()
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.TextField()
    organization_balance = models.DecimalField(max_digits=10, decimal_places=2)
    is_finished = models.BooleanField(default=False)
    is_successful = models.BooleanField(default=False)
    trans_id = models.CharField(max_length=30, blank=True, null=True)
    order_id = models.CharField(max_length=200, blank=True, null=True)
    checkout_request_id = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'
        indexes = [
            models.Index(fields=['created_at']),
        ]

        
    def __str__(self):
        return self.first_name