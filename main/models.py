from django.db import models
from django.contrib.auth.models import User

class TrackerModel(models.Model):
    choices = {
        "I" : "Income",
        "E" : "Expenses"
    }

    date = models.DateField()
    category = models.CharField(max_length=10, choices=choices)
    amount = models.BigIntegerField()
    description = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.date} {self.category} {self.amount} {self.description}'
    
class profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    img = models.ImageField(upload_to='media', default='default.jpg')

    def __str__(self) -> str:
        return f'{self.user.username}'