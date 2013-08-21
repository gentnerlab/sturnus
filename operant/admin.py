from django.contrib import admin
from operant.models import ProtocolType, Protocol, TrialSet, TrialType, TrialClass, Trial


class ProtocolTypeAdmin(admin.ModelAdmin):
    list_display = ('name','description')
admin.site.register(ProtocolType,ProtocolTypeAdmin)

class ProtocolAdmin(admin.ModelAdmin):
    list_display = ('name','type')
admin.site.register(Protocol,ProtocolAdmin)

class TrialSetAdmin(admin.ModelAdmin):
    list_display = ('name','protocol')
admin.site.register(TrialSet,TrialSetAdmin)

class TrialTypeAdmin(admin.ModelAdmin):
    list_display = ('name','description')
admin.site.register(TrialType,TrialTypeAdmin)

class TrialClassAdmin(admin.ModelAdmin):
    list_display = ('name','description')
admin.site.register(TrialClass,TrialClassAdmin)

class TrialAdmin(admin.ModelAdmin):
    list_display = ('index','tr_type','tr_class','stimulus','response','correct','reinforced','trial_set',)
admin.site.register(Trial,TrialAdmin)