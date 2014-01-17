from django.contrib import admin
from mpod.data import models

class PublArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'authors', 'journal', 'year')
    list_filter = ('journal',)
    ordering = ('year',)
    search_fields = ('title', 'authors', 'journal', 'year')
    
    
    def __unicode__(self):
        return str(self.title)+", "+str(self.journal)

class DataFileAdmin(admin.ModelAdmin):
    list_display = ('code','phase_name')
    ordering = ('code',)
    search_fields = ('phase_generic','phase_name')

    def __unicode__(self):
        return str(self.code)+", "+str(self.phase_generic)+", "+str(self.phase_name)

class PropertyAdmin(admin.ModelAdmin):
    list_display = ('tag','name','units')
    ordering = ('tag',)
    search_fields = ('tag','name',)

    def __unicode__(self):
        return str(self.name)+", "+str(self.tag)

class ExperimentalParCondAdmin(admin.ModelAdmin):
    list_display = ('tag','name',)
    ordering = ('tag',)
    search_fields = ('tag','name',)

    def __unicode__(self):
        return str(self.name)+", "+str(self.tag)

##class DataFile_PropertyAdmin(admin.ModelAdmin):
##    list_display = ('datafile','property')
##    ordering = ('datafile',)

##    def __unicode__(self):
##        return str(self.datafile)+", "+str(self.property)

##admin.site.register(models.DataFile_Property, DataFile_PropertyAdmin)
admin.site.register(models.ExperimentalParCond, ExperimentalParCondAdmin)
admin.site.register(models.PublArticle, PublArticleAdmin)
admin.site.register(models.DataFile, DataFileAdmin)
admin.site.register(models.Property, PropertyAdmin)