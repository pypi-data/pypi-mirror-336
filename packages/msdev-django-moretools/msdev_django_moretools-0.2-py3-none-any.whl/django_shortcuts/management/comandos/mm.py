# Comando para ejecutar el comando makemigrations y migrate

from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Comando para ejecutar el comando makemigrations y migrate de todas las aplicaciones del proyecto'

    def handle(self, *args, **options):
        from django.core.management import call_command
        try:
            call_command('makemigrations')
            call_command('migrate')
            self.stdout.write(self.style.SUCCESS('Wii! Todo salió bien, tus migraciones se han hecho correctamente!'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Ups! Algo salió mal al tratar de hacer el trabajo fácil :c ): {e}'))