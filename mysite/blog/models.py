from django.db import models

# Create your models here.
class systemParameter(models.Model):
    parameterName = models.CharField('参数别名',max_length=255)
    parameterKey = models.CharField('参数名',max_length=255)
    parameterValue = models.CharField('参数值',max_length=255)
