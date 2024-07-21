from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Digite a quantidade de propriedades rurais a serem criadas...'

    def add_arguments(self, parser):
        parser.add_argument('quantidade', type=str, help="Ex. 50")

    def handle(self, *args, **options):
        val = options['quantidade']

        print('Realizando a Interseção do mapa de Aptidão com os Cars...')
