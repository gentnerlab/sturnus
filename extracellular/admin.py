from django.contrib import admin
from extracellular.models import CoordinateSystem, Penetration, Location, SortedUnit, Population, SortQualityMethod

class CoordinateSystemAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name','description'),
         }),
        )
admin.site.register(CoordinateSystem,CoordinateSystemAdmin)

class PenetrationAdmin(admin.ModelAdmin):
    list_display = ('hemisphere','rostral','lateral','subject','electrode',)
    list_filter = (
        'subject',
        'subject__sex',
        'electrode',
        'hemisphere',
        'rostral',
        'lateral',
        )
    fieldsets = (
        (None, {
            'fields': ('subject','electrode',),
         }),
        ('Coordinates', {
            'fields': ('hemisphere',('rostral','lateral',),('alpha_angle','beta_angle','rotation_angle'),'depth_max'),
         }),
        ('Meta', {
            'fields': ('name','description','annotations'),
         }),
        ('File information', {
            'fields': ('file_origin',),
         }),
        ('History', {
            'fields': (('created','modified'),),
         }),
        )
    readonly_fields = ('created','modified')
    search_fields = [
        'name',
        'description',
        'annotations',
        'file_origin',
        'subject__name',
        'electrode__serial_number',
        'electrode__notes',
        'electrode__status',
        ]
admin.site.register(Penetration,PenetrationAdmin)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('depth','penetration')
    list_filter = (
        'penetration',
        'depth',
        'blocks',
        )
    fieldsets = (
        (None, {
            'fields': (('penetration','depth'),'blocks'),
         }),
        ('Meta', {
            'fields': ('name','description','annotations'),
         }),
        ('File information', {
            'fields': ('file_origin',),
         }),
        ('History', {
            'fields': (('created','modified'),),
         }),
        )
    filter_horizontal = ['blocks']
    readonly_fields = ('created','modified')
    search_fields = [
        'name',
        'description',
        'annotations',
        'file_origin',
        'penetration__name',
        'penetration__description',
        'penetration__annotations',
        'penetration__file_origin',
        'block__name',
        'block__description',
        'block__annotations',
        'block__file_origin',
        ]
admin.site.register(Location,LocationAdmin)

class SortQualityMethodAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name','description'),
         }),
        )
admin.site.register(SortQualityMethod,SortQualityMethodAdmin)

class SortedUnitAdmin(admin.ModelAdmin):
    list_filter = (
        'recording_channel_group__block',
        'sort_quality',
        'multiunit',
        'population',
        )
    list_display = (
        'recording_channel_group',
        'name',
        'sort_quality',
        'multiunit',
        )
    fieldsets = (
        (None, {
            'fields': ('recording_channel_group','sort_quality','sort_quality_method','multiunit',),
         }),
        ('Event info', {
            'fields': ('name', 'description', 'annotations'),
         }),
        ('File information', {
            'fields': ('file_origin',),
         }),
        ('History', {
            'fields': (('created','modified'),),
         }),
        )
    search_fields = [
        'name',
        'description',
        'annotations',
        'file_origin',
        'recording_channel_group__name',
        'recording_channel_group__description',
        'recording_channel_group__annotations',
        'recording_channel_group__file_origin',
        'recording_channel_group__block__name',
        'recording_channel_group__block__description',
        'recording_channel_group__block__annotations',
        'recording_channel_group__block__file_origin',
        ]
    # inlines = [SpikeTrainInline,]
    readonly_fields = ('created','modified')
    class Media:
        js = ('/js/jquery.sparkline.min.js',)
admin.site.register(SortedUnit,SortedUnitAdmin)

class PopulationAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('units',),
         }),
        ('Meta', {
            'fields': ('name','description','annotations'),
         }),
        ('File information', {
            'fields': ('file_origin',),
         }),
        ('History', {
            'fields': (('created','modified'),),
         }),
        )
    filter_horizontal = ['units']
    readonly_fields = ('created','modified')
admin.site.register(Population,PopulationAdmin)
