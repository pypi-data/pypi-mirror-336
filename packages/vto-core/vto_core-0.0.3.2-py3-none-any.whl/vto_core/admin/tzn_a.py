from django.contrib import admin

from vto_core.models import TZWikiSlug
from vto_core.models import TZAbbreviation
from vto_core.models import TimeZone

# admin.site.register()

@admin.register(TZWikiSlug)
class TZWikiAdmin(admin.ModelAdmin):
    list_display = [ 'slug', ]
    search_fields = ['slug', ]

@admin.register(TZAbbreviation)
class TZAbbrAdmin(admin.ModelAdmin):
    autocomplete_fields = ['wiki_slug']
    list_display = [
        'offset',
        'abbr',
        'identifier',
        'wiki_slug',
    ]
    list_display_links = ['identifier']
    search_fields = [
        'identifier',
        'abbr',
    ]

@admin.register(TimeZone)
class TZAdmin(admin.ModelAdmin):
    autocomplete_fields = [
        'std',
        'dst',
    ]
    list_display = [
        'identifier',
        'tz_type',
        'src_file',
        'std',
        'dst',
        'aliases',
    ]
    search_fields = [
        'identifier',
        'std__identifier',
        'dst__identifier',
    ]