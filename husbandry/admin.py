from django.contrib import admin
from husbandry.models import Subject, Record, Location

class RecordInline(admin.StackedInline):
    model = Record
    extra = 0

# class LocationInline(admin.TabularInline):
#     model = Location


class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'sex',
        'origin',
        'location',
        'health',
        'weight',
        )
    list_filter = ('origin','sex')
    search_fields = [
        'name',
        'origin',
        'records__notes'
        ]
    inlines = [
        RecordInline,
        ]

    def location(self,obj):
        return obj.records.latest().location.name
    location.short_description = 'Location'

    def health(self,obj):
        return obj.records.latest().health
    health.short_description = 'Health'

    def weight(self,obj):
        return obj.records.latest().weight
    weight.short_description = 'Weight (g)'

admin.site.register(Subject,SubjectAdmin)

class RecordAdmin(admin.ModelAdmin):
    list_display = (
        'intervention',
        'datetime',
        'subject',
        'health',
        'weight',
        'location',
        )
    search_fields = [
        'subject__name',
        'subject__description',
        'subject__origin__name',
        'subject__origin__description',
        'notes'
        'location__name',
        'health',
        'intervention',
        ]
    list_filter = ('datetime','subject')
    readonly_fields = ('created','modified')
admin.site.register(Record,RecordAdmin)

class LocationAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'description',
        'n_subjects',
        )
    search_fields = [
        'name',
        'description',
        'subjects_from_here__name',
        ]
    inlines = [
        RecordInline,
        ]
    list_filter = ('subjects_from_here__name','records__subject__name')

    def n_subjects(self,obj):
        return Subject.objects.filter(records__location=obj).count()
    n_subjects.short_description = 'Number of Subjects'

admin.site.register(Location,LocationAdmin)