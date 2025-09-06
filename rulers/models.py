from django.db import models

# Create your models here.
class Capital(models.Model):
    name = models.CharField(max_length=100)
    start_year = models.IntegerField()
    end_year = models.IntegerField()

    class Meta :
        unique_together = ('start_year', 'end_year')

    def __str__(self) :
        return f'{self.name} ({self.start_year}-{self.end_year})'

class Monarch(models.Model):
    name = models.CharField(max_length=200)
    family = models.CharField(max_length=200, null=True, blank=True)
    start_year = models.IntegerField()
    end_year = models.IntegerField()
    capital = models.ForeignKey(Capital, on_delete=models.SET_NULL, null=True, related_name='monarchs')

    class Meta :
        unique_together = ('start_year', 'end_year')

    def __str__(self) :
        return f'{self.name} ({self.start_year}-{self.end_year})'