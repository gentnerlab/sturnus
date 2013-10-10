from django.contrib import admin
from husbandry.models import Subject, Observation

class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'sex',
        'origin',
        )
    search_fields = [
        'name',
        'origin',
        'observation_set__notes'
        ]
    list_filter = ('origin','sex')
admin.site.register(Subject,SubjectAdmin)

class ObservationAdmin(admin.ModelAdmin):
    list_display = (
        'datetime',
        'subject',
        'weight',
        'notes',
        )
    search_fields = [
        'subject__name',
        'subject__origin',
        'notes'
        ]
    list_filter = ('datetime','subject')
admin.site.register(Observation,ObservationAdmin)
