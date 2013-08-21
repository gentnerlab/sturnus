from django.contrib import admin
from electrode.models import Electrode



# class  ElectrodeModelAdmin(admin.ModelAdmin):
#     list_display = (
#         'manufacturer',
#         'model_number',
#         )
# admin.site.register(ElectrodeModel,ElectrodeModelAdmin)

# class RecordingSiteModelAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(RecordingSiteModel,RecordingSiteModelAdmin)
    
class ElectrodeAdmin(admin.ModelAdmin):
    list_display = (
        'serial_number',
        # 'electrode_model',
        # 'batch',
        'status',
        'uses',
        'notes',
        )
admin.site.register(Electrode,ElectrodeAdmin)

# class RecordingSiteAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(RecordingSite,RecordingSiteAdmin)

# class ExtendedRecordingChannelAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(ExtendedRecordingChannel,ExtendedRecordingChannelAdmin)

# class ElectrodeBatchAdmin(admin.ModelAdmin):
#     pass
# admin.site.register(ElectrodeBatch,ElectrodeBatchAdmin)

