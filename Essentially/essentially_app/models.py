from django.db import models
from django.utils.timezone import now
# Create your models here.

class ClassSession(models.Model):
    count = models.IntegerField()
    time = models.IntegerField(default=110)
    date = models.DateField(default=now)

    CLASS_TYPE_CHOICES = [
        ('IP', 'In-Person'),
        ('ON', 'Online'),
    ]
    class_type = models.CharField(max_length=2, choices=CLASS_TYPE_CHOICES)

    @property
    def average(self):
        return self.count / self.time
    
    def __str__(self):
        return f"{self.count} | {self.get_class_type_display()} | {self.date}"

