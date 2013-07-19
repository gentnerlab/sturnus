from sturnus.models import *
from django.contrib import admin


"""models"""
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'sex',)
admin.site.register(Subject, SubjectAdmin)


class PenetrationAdmin(admin.ModelAdmin):
    list_display = (
        'hemisphere',
        'rostral',
        'lateral',
        'alpha_angle',
        'beta_angle',
        'rotation_angle',
        'depth_max',
        )   
admin.site.register(Penetration, PenetrationAdmin)