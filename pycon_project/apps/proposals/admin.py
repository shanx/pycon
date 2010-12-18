import csv
import time

from django.http import HttpResponse
from django.utils.functional import update_wrapper

from django.contrib import admin

from proposals.models import Proposal, ProposalSessionType

from review.models import ProposalResult

admin.site.register(ProposalSessionType)

class ProposalAdmin(admin.ModelAdmin):
    list_display = [
        "title", "session_type", "audience_level", 
        "cancelled", "extreme_pycon", "invited"
    ]
    
    def get_urls(self):
        from django.conf.urls.defaults import patterns, url

        urlpatterns = super(ProposalAdmin, self).get_urls()

        def wrap(view):
            def wrapper(*args, **kwargs):
                return self.admin_site.admin_view(view)(*args, **kwargs)
            return update_wrapper(wrapper, view)

        info = self.model._meta.app_label, self.model._meta.module_name

        return patterns("",
            url(r"^csv/$",
                wrap(self.csv),
                name="%s_%s_csv" % info
            )
        ) + urlpatterns
    
    def csv(self, request):
        response = HttpResponse(mimetype="text/csv")
        writer = csv.writer(response)
        
        filename = "talks-%s.csv" % time.strftime("%Y-%m-%d")
        response["Content-Disposition"] = "attachment; filename=%s" % filename
        
        talks = Proposal.objects.filter(
            session_type__in=[Proposal.SESSION_TYPE_TALK, Proposal.SESSION_TYPE_PANEL]
        )
        
        for talk in talks:
            writer.writerow([
                talk.id, talk.title, talk.speaker.name,
                talk.get_audience_level_display(), talk.invited,
                talk.extreme_pycon, talk.result.plus_one,
                talk.result.plus_zero, talk.result.minus_zero,
                talk.result.minus_one,
            ])
        return response

admin.site.register(Proposal, ProposalAdmin)