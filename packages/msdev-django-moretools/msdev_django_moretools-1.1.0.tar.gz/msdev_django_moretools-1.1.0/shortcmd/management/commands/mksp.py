from django.core.management.base import BaseCommand
from django.core.management import call_command
# Crear un superusuario automáticamente
from django.contrib.auth.models import User
from django.db.utils import IntegrityError
import os

class Command(BaseCommand):
    help = 'Crea un superusuario automáticamente'

    def add_arguments(self, parser):
        parser.add_argument(
            '--username',
            dest='username',
            help='Nombre de usuario del superusuario'
        )
        parser.add_argument(
            '--password',
            dest='password',
            help='Contraseña del superusuario'
        )

    def handle(self, *args, **options):
        username = options['username']
        password = options['password']

        if not username:
            username = input('Nombre de usuario: ')
        if not password:
            password = input('Contraseña: ')

        try:
            user = User.objects.create_superuser(username, password)
            self.stdout.write(self.style.SUCCESS(
                f"Superusuario '{username}' creado correctamente"
            ))
        except IntegrityError:
            self.stdout.write(self.style.ERROR(
                f"El superusuario '{username}' ya existe"
            ))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error al crear el superusuario:"))
            self.stdout.write(self.style.ERROR(f"Detalles: {str(e)}"))