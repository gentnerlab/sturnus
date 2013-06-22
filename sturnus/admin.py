from sturnus.models import *
from django.contrib import admin

"""inlines"""
class BlockInline(admin.StackedInline):
    model = Block

class BehaviorTrialInline(admin.TabularInline):
    model = BehaviorTrial

class EventInline(admin.TabularInline):
    model = Event

class ElectrodePadModelInline(admin.TabularInline):
    model = ElectrodePadModel

class ElectrodePadInline(admin.TabularInline):
    model = ElectrodePad

class SiteInline(admin.TabularInline):
    model = Site

class SortChannelInline(admin.TabularInline):
    model = SortChannel
    extra = 4
    max_num = 4

class SpikeTrainInline(admin.TabularInline):
    model = SpikeTrain

"""models"""
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'sex',)
    inlines = [
        BlockInline,
        ]
admin.site.register(Subject, SubjectAdmin)

class BlockAdmin(admin.ModelAdmin):
    list_display = ('datetime','title', 'desc', 'subject',)
    inlines = [
        BehaviorTrialInline,
        ]
admin.site.register(Block, BlockAdmin)

class BehaviorTrialAdmin(admin.ModelAdmin):
    list_display = ('tr_num','datetime','block','tr_type','tr_class','response','feed','timeout',)
    inlines = [
        EventInline,
        ]
admin.site.register(BehaviorTrial, BehaviorTrialAdmin)

class EventTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(EventType, EventTypeAdmin)

class EventAdmin(admin.ModelAdmin):
    list_display = ('trial','datetime','event_type','desc',)
admin.site.register(Event, EventAdmin)

class StimulusAdmin(admin.ModelAdmin):
    pass
admin.site.register(Stimulus, StimulusAdmin)

class EpochTypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(EpochType, EpochTypeAdmin)

class EpochAdmin(admin.ModelAdmin):
    list_display = ('trial','start','end','desc',)
admin.site.register(Epoch, EpochAdmin)

class ElectrodeModelAdmin(admin.ModelAdmin):
    list_display = ('manufacturer','model_number',)
    inlines = [
        ElectrodePadModelInline,
        ]
admin.site.register(ElectrodeModel, ElectrodeModelAdmin)

class ElectrodePadModelAdmin(admin.ModelAdmin):
    list_display = ('size','x_coord','y_coord',)
admin.site.register(ElectrodePadModel, ElectrodePadModelAdmin)

class ElectrodeAdmin(admin.ModelAdmin):
    list_display = ('serial_number',)
    inlines = [
        ElectrodePadInline,
        ]
admin.site.register(Electrode, ElectrodeAdmin)

class ElectrodePadAdmin(admin.ModelAdmin):
    list_display = ('impedance','electrode','electrode_pad_model',)
admin.site.register(ElectrodePad, ElectrodePadAdmin)

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
    inlines = [
        SiteInline,
        ]
admin.site.register(Penetration, PenetrationAdmin)

class SiteAdmin(admin.ModelAdmin):
    list_display = ('penetration','depth',)
admin.site.register(Site, SiteAdmin)

class RegionAdmin(admin.ModelAdmin):
    list_display = ('abbrev','name','is_part_of','url',)
admin.site.register(Region, RegionAdmin)

class RecordingChannelAdmin(admin.ModelAdmin):
    list_display = ('site','pad','region',)
admin.site.register(RecordingChannel, RecordingChannelAdmin)

class SortAdmin(admin.ModelAdmin):
    inlines = [
        SortChannelInline,
        ]
admin.site.register(Sort, SortAdmin)

class IsolationAdmin(admin.ModelAdmin):
    list_display = ('sort','num_units','confidence',)
admin.site.register(Isolation, IsolationAdmin)

class SpikeTrainAdmin(admin.ModelAdmin):
    list_display = ('t_start','t_stop','isolation','unit',)
admin.site.register(SpikeTrain, SpikeTrainAdmin)

class UnitAdmin(admin.ModelAdmin):
    list_display = ('label',)
    inlines = [
        SpikeTrainInline,
        ]
admin.site.register(Unit, UnitAdmin)


