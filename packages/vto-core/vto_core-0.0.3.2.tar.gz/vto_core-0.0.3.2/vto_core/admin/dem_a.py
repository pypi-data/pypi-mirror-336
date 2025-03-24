from datetime import datetime as dtm
from zoneinfo import ZoneInfo as zi
from django.conf import settings
from django.contrib import admin

from vto_core.models import DemoExchange, DemoTestTimestamp


@admin.register(DemoExchange)
class DemoExchangeAdmin(admin.ModelAdmin):
    autocomplete_fields = ['tz']
    list_display = [ 'abbr', 'name_long', 'tz' ]


@admin.register(DemoTestTimestamp)
class DemoTestTSAdmin(admin.ModelAdmin):
    list_display = [
        'ts_unix',
        'dst',

        'ts_utc',
        'get_utc',

        'get_utc_adm',

        'exchange',
        'exchange__tz',
    ]
    readonly_fields = [
        'ts_utc',
    ]


    #'''
    def get_utc_adm(self, obj):
        utca = dtm.fromtimestamp(obj.ts_unix, tz=zi('UTC'))
        return utca.strftime(settings.TSFMT)

    # get_utc_adm.admin_order_field = 'project__name'
    get_utc_adm.admin_order_field = 'ts_unix'
    # '''
