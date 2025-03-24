from datetime import datetime as dtm
from zoneinfo import ZoneInfo as zi
from django.conf import settings
from django.views.generic import ListView 
from vto_core.models import DemoTestTimestamp


class DemoTestTSList(ListView):
    model = DemoTestTimestamp
    template_name = 'time/demo-ts-list.dtl'

    def calc_utc(self, obj):
        utcv = dtm.fromtimestamp(obj.ts_unix, tz=zi('Etc/UTC'))
        return utcv.strftime(settings.TSFMT)

    def calc_user_local(self, obj):
        usrv = dtm.fromtimestamp(obj.ts_unix, \
            tz=zi(str(self.request.user.timezone.identifier)))
        return usrv.strftime(settings.TSFMT)

    def calc_exchange_local(self, obj):
        xchv = dtm.fromtimestamp(obj.ts_unix, tz=zi(obj.exchange.tz.identifier))
        return xchv.strftime(settings.TSFMT)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        for obj in context['object_list']:
            obj.tsv_utc = self.calc_utc(obj)
            if self.request.user.is_authenticated:
                obj.tsv_usr = self.calc_user_local(obj)
            obj.tsv_xch = self.calc_exchange_local(obj)
        return context