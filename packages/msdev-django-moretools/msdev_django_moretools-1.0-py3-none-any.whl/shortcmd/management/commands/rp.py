from django.core.management.base import BaseCommand
from django.core.management import call_command
from django.conf import settings

# Comando para ejecutar el servidor de desarrollo de forma publica en la red local con un puerto especifico

class Command(BaseCommand):
    help = 'Run the development server publicly on the local network using this command'
    
    def add_arguments(self, parser):
        parser.add_argument('port', nargs='?', type=int, help='Port to run the server on')
    
    def handle(self, *args, **kwargs):
        port = kwargs.get('port') or 8000
        # Aqui se ejecuta el servidor de desarrollo de Django
        self.stdout.write(self.style.SUCCESS(f'Launching public development server accessible on local network at port {port}'))
        try:
            call_command(
                'runserver',
                f'0.0.0.0:{port}',
                verbosity=0,
                use_reloader=True,
                use_ipv6=False,
                use_threading=True
            ),
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Oh no! This isn't a package error, you need to fix your code.\nDetails:\n{e}"))