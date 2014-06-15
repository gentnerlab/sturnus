from django.contrib import admin
from operant.models import ProtocolType, Protocol, Session, TrialType, TrialClass, Trial


class ProtocolTypeAdmin(admin.ModelAdmin):
    list_display = ('name','description')
admin.site.register(ProtocolType,ProtocolTypeAdmin)

class ProtocolAdmin(admin.ModelAdmin):
    list_display = ('name','type')
admin.site.register(Protocol,ProtocolAdmin)

class SessionAdmin(admin.ModelAdmin):
    list_display = ('name','protocol','accuracy')
    actions = ['calc_performance']

    def save_model(self, request, obj, form, change):
        obj.calc()
        obj.save()

    def calc_performance(self, request, queryset):
        for session in queryset:
            session.calc()
            session.save()
    calc_performance.short_description = "Calculate the performance of the selected sessions"

admin.site.register(Session,SessionAdmin)

class TrialTypeAdmin(admin.ModelAdmin):
    list_display = ('name','description')
admin.site.register(TrialType,TrialTypeAdmin)

class TrialClassAdmin(admin.ModelAdmin):
    list_display = ('name','description')
admin.site.register(TrialClass,TrialClassAdmin)

class TrialAdmin(admin.ModelAdmin):
    list_display = ('index','tr_type','tr_class','stimulus','response','correct','reinforced','session',)
admin.site.register(Trial,TrialAdmin)