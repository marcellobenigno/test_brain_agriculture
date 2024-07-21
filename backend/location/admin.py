from django.contrib import admin
from easy_select2 import select2_modelform

from .models import State, City


@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['state', 'abbreviation', 'geocode', 'active', 'created', 'updated', ]
    search_fields = ['state', ]
    list_filter = ['state']
    form = select2_modelform(State, attrs={'width': '600px'})


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['city', 'state', 'geocode', 'active', 'created', 'updated', ]
    search_fields = ['city', ]
    form = select2_modelform(City, attrs={'width': '600px'})
