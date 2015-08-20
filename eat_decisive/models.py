from django.db import models
from django.forms import ModelForm

class LatestQuery(models.Model):
    searched = models.CharField(max_length=128)
#    def save(self, *args, **kwargs):
#        super(LatestQuery, self).save(*args, **kwargs)

    def __unicode__(self):      #For Python 2, use __str__ on Python 3
        return self.searched


class QueryForm(ModelForm):
    class Meta:
        model = LatestQuery
        fields = ['searched']

        
