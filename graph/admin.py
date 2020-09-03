from django.contrib import admin
from graph.models import Unit, DataNode, DataEdge


class UnitAdmin(admin.ModelAdmin):
    model = Unit
    list_display = ('name',)


class DataNodeAdmin(admin.ModelAdmin):
    model = DataNode
    list_display = ('id', 'title', 'name', 'type', 'unit')
    list_filter = ('type',)
    search_fields = ('title', 'name')


class DataEdgeAdmin(admin.ModelAdmin):
    model = DataEdge
    list_display = ('id', 'source', 'dest')


admin.site.register(Unit, UnitAdmin)
admin.site.register(DataNode, DataNodeAdmin)
admin.site.register(DataEdge, DataEdgeAdmin)
