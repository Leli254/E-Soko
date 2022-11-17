from django.db import models

class Contact(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email_address = models.EmailField(max_length=150)
    message = models.CharField(max_length=2000)

    def __str__(self):
        return self.first_name
    
    class Meta:
        verbose_name='Contact'
        verbose_name_plural = 'Contacts'

class Subscriber(models.Model):
    email = models.CharField(unique=True, max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Newsletter Subscriber'
        verbose_name_plural = 'Newsletter Subscribers'

    def __str__(self):
        return '%s' % self.email


class Feedback(models.Model):
    name=models.CharField(max_length=40)
    feedback=models.CharField(max_length=500)
    email=models.EmailField(max_length=100)
    date= models.DateField(auto_now_add=True,null=True)

    class Meta:
        verbose_name='Feedback'
        verbose_name_plural = 'Feedbacks'

    def __str__(self):
        return self.name