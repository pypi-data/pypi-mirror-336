from datetime import datetime as dtm
from zoneinfo import ZoneInfo as zi
from django.db import models
from djinntoux.abstract_models import UUIDpk7


class DemoExchange(UUIDpk7):

    abbr = models.CharField(max_length=14, unique=True)

    name_long = models.CharField(max_length=30, unique=True)

    tz = models.ForeignKey('TimeZone', on_delete=models.PROTECT,
        null=True, blank=True)

    class Meta:
        ordering = ['name_long']
        verbose_name_plural = 'ZZZ — Demo stock exchanges'

    def __str__(self):
        return self.abbr


''' samples
before DST: 1741035602 (03 March 2025)
during DST: 1741964552 (14 March 2025)
'''
class DemoTestTimestamp(models.Model):

    exchange = models.ForeignKey('DemoExchange', on_delete=models.PROTECT,
        to_field='abbr', default='NYSE')

    dst = models.BooleanField(default=False)

    ts_unix = models.PositiveIntegerField(help_text='1741035602')

    ts_utc = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['ts_unix']
        verbose_name_plural = 'ZZZ — Demo test time stamps'
    
    def __str__(self):
        return str(self.ts_unix)
    
    def get_utc(self):
        """Convert Unix timestamp to UTC datetime"""
        if not self.ts_unix:
            return None
        
        try:
            # Create a timezone-aware UTC datetime from the Unix timestamp
            return dtm.fromtimestamp(self.ts_unix, tz=zi('UTC'))
        except (TypeError, ValueError) as e:
            print(f"Error converting to UTC: {e}")
            return None
    
    def save(self, *args, **kwargs):
        self.ts_utc = self.get_utc()
        super(DemoTestTimestamp, self).save(*args, **kwargs)
