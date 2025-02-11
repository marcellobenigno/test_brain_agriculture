# Generated by Django 5.0.7 on 2024-07-22 10:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(blank=True, default=True, verbose_name='Ativo')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Modificado')),
                ('state', models.CharField(max_length=100, verbose_name='Estado')),
                ('abbreviation', models.CharField(max_length=2, unique=True, verbose_name='Sigla')),
                ('geocode', models.IntegerField(verbose_name='Geocódigo')),
            ],
            options={
                'verbose_name': 'Estado',
                'verbose_name_plural': 'Estados',
                'ordering': ['state'],
            },
        ),
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(blank=True, default=True, verbose_name='Ativo')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Criado')),
                ('updated', models.DateTimeField(auto_now=True, verbose_name='Modificado')),
                ('city', models.CharField(max_length=100, verbose_name='Cidade')),
                ('geocode', models.IntegerField(verbose_name='Geocódigo')),
                ('state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='location.state', verbose_name='Estado')),
            ],
            options={
                'verbose_name': 'Cidade',
                'verbose_name_plural': 'Cidades',
                'ordering': ['state', 'city'],
            },
        ),
    ]
