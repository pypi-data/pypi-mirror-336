from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

# Comando para hacer migraciones y luego migrar

class Command(BaseCommand):
    help = 'Make migrations and migrate the database at once using this command'
    
    def handle(self, *args, **kwargs):
        try:
            call_command('makemigrations')
            call_command('migrate')
            self.stdout.write(self.style.SUCCESS('Migrations and database migration completed successfully c: '))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Oh no! This isn't a package error, you need to fix your code.\nDetails:\n{e}"))