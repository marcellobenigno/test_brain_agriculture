# Generated by Django 5.0.7 on 2024-07-22 10:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('farmer', '0001_initial'),
        ('location', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RuralProperty',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(blank=True, default=True, verbose_name='Ativo')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Modificado')),
                ('property_name', models.CharField(max_length=255, verbose_name='Nome da Propriedade')),
                ('area_ha', models.DecimalField(decimal_places=3, max_digits=10, verbose_name='Área da Propridedade')),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='location.city', verbose_name='cidade')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='farmer.farmer', verbose_name='proprietário')),
            ],
            options={
                'verbose_name': 'Propriedade Rural',
                'verbose_name_plural': 'Propriedades Rurais',
            },
        ),
        migrations.CreateModel(
            name='Plantation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(blank=True, default=True, verbose_name='Ativo')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Modificado')),
                ('name', models.CharField(choices=[('Algodão', 'Algodão'), ('Café', 'Café'), ('Cana de Açúcar', 'Cana de Açúcar'), ('Milho', 'Milho'), ('Soja', 'Soja'), ('Área de Vegetação', 'Área de Vegetação')], max_length=50, verbose_name='Nome da Cultura')),
                ('area_ha', models.DecimalField(decimal_places=3, max_digits=10, verbose_name='Área (ha)')),
                ('rural_property', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rural_property.ruralproperty', verbose_name='Propriedade Rural')),
            ],
            options={
                'verbose_name': 'Área agricultável',
                'verbose_name_plural': 'Áreas agricultáveis',
            },
        ),
    ]
