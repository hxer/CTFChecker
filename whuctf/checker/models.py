import json
from django.db import models


# Create your models here.
class Team(models.Model):
    tid = models.PositiveIntegerField()
    name = models.CharField(max_length=200)
    status = models.CharField(max_length=100)
    round = models.PositiveIntegerField()
    time = models.CharField(max_length=50)
    count = models.CharField(max_length=100)
    score = models.IntegerField(default=0)


    def setstatus(self, x):
        self.status = json.dumps(x)

    def getstatus(self):
        return json.loads(self.status)
    
    def setcount(self, x):
        self.count = json.dumps(x)

    def getcount(self):
        return json.loads(self.count)
