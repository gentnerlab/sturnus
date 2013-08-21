from django.contrib import admin
from husbandry.models import Subject

class SubjectAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'sex',
        'origin',
        )
admin.site.register(Subject,SubjectAdmin)