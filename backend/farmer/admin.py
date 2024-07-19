from django.contrib import admin
from easy_select2 import select2_modelform

from .models import Farmer


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = ['name', 'cpf', 'cnpj', 'active', 'created', 'updated', ]
    search_fields = ['name', 'cpf']
    list_filter = ['active']
    form = select2_modelform(Farmer, attrs={'width': '600px'})
