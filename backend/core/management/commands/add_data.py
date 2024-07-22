import os
import random
from decimal import Decimal

import pandas as pd
from django.core.management.base import BaseCommand
from faker import Faker

from backend.farmer.models import Farmer
from backend.location.models import City, State
from backend.rural_property.models import RuralProperty, Plantation
from backend.settings import BASE_DIR


class Command(BaseCommand):
    help = 'Specify the number of rural properties to create...'

    def add_arguments(self, parser):
        parser.add_argument('quantidade', type=int, nargs='?', default=50, help="Ex. 50")

    def handle(self, *args, **options):
        num = options['quantidade']

        num_cities = City.objects.count()
        num_states = State.objects.count()

        faker = Faker('pt_BR')

        if not num_cities and not num_states:
            cities_csv = os.path.join(BASE_DIR, 'data', 'cities.csv')
            states_csv = os.path.join(BASE_DIR, 'data', 'states.csv')
            df_states = pd.read_csv(states_csv)
            df_cities = pd.read_csv(cities_csv)

            # Create States
            state_objects = []
            for idx, row in df_states.iterrows():
                obj = State(
                    state=row['nome'],
                    abbreviation=row['sigla'],
                    geocode=row['geocodigo']
                )
                state_objects.append(obj)

            State.objects.bulk_create(state_objects)

            # Create Cities
            city_objects = []
            for idx, row in df_cities.iterrows():
                state = State.objects.filter(geocode=row['cod_uf']).first()
                # Load only cities of São Paulo State
                if state and state.geocode == 35:
                    obj = City(
                        state=state,
                        city=row['nome'],
                        geocode=row['geocodigo']
                    )
                    city_objects.append(obj)

            City.objects.bulk_create(city_objects)

            print('Cities and States loaded successfully!')

        num_farmers = Farmer.objects.count()

        if not num_farmers:
            farmer_objects = []
            for i in range(num):
                if random.choice([True, False]):
                    cpf = faker.cpf().replace('.', '').replace('-', '')
                    cnpj = None
                else:
                    cpf = None
                    cnpj = faker.cnpj().replace('.', '').replace('/', '').replace('-', '')
                obj = Farmer(
                    name=f'{faker.first_name()} {faker.last_name()}',
                    cpf=cpf,
                    cnpj=cnpj
                )
                farmer_objects.append(obj)

            Farmer.objects.bulk_create(farmer_objects)

            print(f'Added {num} Rural Owners successfully!')

        num_rural_properties = RuralProperty.objects.count()

        if not num_rural_properties:
            farmers = Farmer.objects.all()
            for farmer in farmers:
                city = City.objects.order_by('?').first()
                property_name = faker.company()
                area_ha = Decimal(random.uniform(30, 1000)).quantize(Decimal('1.000'))

                rural_property = RuralProperty(
                    owner=farmer,
                    city=city,
                    property_name=property_name,
                    area_ha=area_ha
                )
                rural_property.save()

                # Generate Plantations

                min_plantation_area = Decimal('5.000')

                while area_ha > 0:
                    max_plantation_area = min(area_ha, min_plantation_area * 2)

                    if max_plantation_area < min_plantation_area:
                        break

                    plantation_area = Decimal(random.uniform(0, float(area_ha))).quantize(Decimal('1.000'))
                    plantation_name = random.choice([choice[0] for choice in Plantation.CULTURE_CHOICES])

                    if plantation_area > 0:
                        plantation = Plantation(
                            name=plantation_name,
                            area_ha=plantation_area,
                            rural_property=rural_property
                        )
                        plantation.save()
                        area_ha -= plantation_area

                print(
                    f'Generated RuralProperty: {rural_property.property_name} with total area {rural_property.area_ha} ha')
                for plantation in Plantation.objects.filter(rural_property=rural_property):
                    print(f'Generated Plantation: {plantation.name} with area {plantation.area_ha} ha')
