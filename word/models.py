from django.db import models

# Create your models here.
from django.db import models
import os



# Create your models here.
class Text(models.Model):
    path = models.FilePathField()

    def __unicode__(self):
        return u'%s' % self.path

    def get_upload_to(self):
        return u'your file path is %s' %self.path


