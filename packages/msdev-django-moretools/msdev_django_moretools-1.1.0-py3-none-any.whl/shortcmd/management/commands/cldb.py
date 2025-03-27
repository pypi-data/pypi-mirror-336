from django.core.management.base import BaseCommand
from django.core.management import call_command
import os

class Command(BaseCommand):
    help = 'Genera modelos Django a partir de una base de datos existente'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--output', 
            dest='output',
            default='models.py',
            help='Archivo donde guardar los modelos generados (predeterminado: models.py)'
        )
        parser.add_argument(
            'tables', 
            nargs='*',
            help='Tablas específicas a inspeccionar (opcional)'
        )
        parser.add_argument(
            '--app', 
            dest='app',
            help='Aplicación donde guardar los modelos (opcional)'
        )
    
    def handle(self, *args, **options):
        tables = options['tables']
        output_file = options['output']
        app = options['app']
        
        # Ajustar la ruta de salida si se especifica una aplicación
        if app:
            app_models_dir = os.path.join('apps', app, 'models')
            if not os.path.exists(app_models_dir):
                os.makedirs(app_models_dir)
            output_file = os.path.join(app_models_dir, output_file)
        
        try:
            self.stdout.write(f"Inspeccionando la base de datos...")
            
            # Preparar los argumentos para inspectdb
            inspectdb_args = list(tables)  # Convertir a lista para poder modificarla
            
            # Ejecutar inspectdb y guardar la salida en el archivo
            with open(output_file, 'w') as f:
                # Redirigir la salida de inspectdb al archivo
                call_command('inspectdb', *inspectdb_args, stdout=f)
            
            self.stdout.write(self.style.SUCCESS(
                f"Modelos generados correctamente en '{output_file}'"
            ))
            self.stdout.write(self.style.WARNING(
                f"Nota: Revisa los modelos generados, ya que pueden requerir ajustes manuales."
            ))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error al generar los modelos:"))
            self.stdout.write(self.style.ERROR(f"Detalles: {str(e)}"))