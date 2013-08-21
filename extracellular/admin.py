from django.contrib import admin
from extracellular.models import CoordinateSystem, Penetration, Location, Unit, Population, SortQualityMethod

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
admin.site.register(Penetration,PenetrationAdmin)

class LocationAdmin(admin.ModelAdmin):
    list_display = ('depth','penetration')
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
admin.site.register(Location,LocationAdmin)

class SortQualityMethodAdmin(admin.ModelAdmin):
    list_display = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name','description'),
         }),
        )
admin.site.register(SortQualityMethod,SortQualityMethodAdmin)

class UnitAdmin(admin.ModelAdmin):
    list_filter = (
        'recording_channel_group__block',
        'sort_quality',
        'multiunit',
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
admin.site.register(Unit,UnitAdmin)

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
    readonly_fields = ('created','modified')
admin.site.register(Population,PopulationAdmin)