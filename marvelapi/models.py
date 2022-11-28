from django.db import models



#fetch data from api






class Marvel(models.Model):
    character = models.CharField(max_length=200, default='')
    
    
    def __str__(self):
        return self.character