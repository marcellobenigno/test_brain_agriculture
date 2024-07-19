from django.contrib import admin
from easy_select2 import select2_modelform

from .models import Plantation, RuralProperty


@admin.register(Plantation)
class PlantationAdmin(admin.ModelAdmin):
    list_display = ['name', 'area_ha', 'rural_property', 'active', 'created', 'updated', ]
    search_fields = ['name', ]
    list_filter = ['name']
    form = select2_modelform(Plantation, attrs={'width': '600px'})


class PlantationInline(admin.TabularInline):
    model = Plantation
    extra = 1


@admin.register(RuralProperty)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ['property_name', 'owner', 'city', 'total_area_ha', 'vegetation_area_ha', 'active', 'created',
                    'updated', ]
    search_fields = ['property_name', ]
    form = select2_modelform(RuralProperty, attrs={'width': '600px'})
    inlines = [PlantationInline, ]
