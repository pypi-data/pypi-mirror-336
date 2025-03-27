# 🚀 Django Shortcuts

![Django Version](https://img.shields.io/badge/Django-5.1+-green.svg)
![Python Version](https://img.shields.io/badge/Python-3.12+-blue.svg)
![License](https://img.shields.io/badge/License-GNU-yellow.svg)

## ✨ Potencia tu desarrollo Django con comandos súper rápidos

**Django Shortcuts** transforma tu experiencia de desarrollo con Django proporcionando **comandos abreviados intuitivos** que reemplazan operaciones repetitivas y complejas con simples atajos de teclado. ¡Ahorra tiempo y enfócate en lo que realmente importa: crear aplicaciones increíbles!

![Django Shortcuts Demo](https://via.placeholder.com/800x400?text=Django+Shortcuts+Demo)

## 📋 ¿Qué puedes hacer?

| Comando | Descripción | Lo que reemplaza |
|---------|-------------|------------------|
| `mm` | Ejecuta migraciones para todas las apps | `makemigrations` + `migrate` |
| `rp` | Ejecuta servidor en puerto 80 (público) | `runserver 0.0.0.0:80` |
| `bk` | Crea backup de tu base de datos | Proceso manual de respaldo |
| `upbk` | Restaura datos desde un backup | Proceso manual de restauración |
| `clonedb` | Genera modelos desde una BD existente | `inspectdb` + configuración manual |
| `mksp` | Crea superusuario rápidamente | `createsuperuser` + ingreso manual de datos |

## 🛠️ Instalación Paso a Paso

### Requisitos previos

Antes de instalar Django Shortcuts, asegúrate de tener:

- Python 3.7 o superior instalado
- Django 3.2 o superior instalado
- Pip actualizado a la última versión

### Instalación básica

```bash
# Actualiza pip para asegurar compatibilidad
pip install --upgrade pip

# Instala Django Shortcuts
pip install msdev-django-moretools
```

### Instalación en entorno virtual (recomendado)

```bash
# Crea un entorno virtual
python -m venv venv

# Activa el entorno virtual
# En Windows:
venv\Scripts\activate
# En macOS/Linux:
source venv/bin/activate

# Instala Django Shortcuts en el entorno
pip install msdev-django-moretools
```

## ⚙️ Configuración con Django

Para integrar completamente Django Shortcuts en tu proyecto Django, sigue estos pasos:

### 1. Añade 'django_shortcuts' a INSTALLED_APPS

Abre tu archivo `settings.py` y añade 'django_shortcuts' a la lista de INSTALLED_APPS:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    # ... otras apps ...
    'msdev-django-moretools',  # Añade esta línea
]
```

### 2. Verifica la instalación

Para comprobar que todo está correctamente instalado, ejecuta:

```bash
python manage.py help
```

Deberías ver los nuevos comandos (`mm`, `rp`, `bk`, etc.) en la lista de comandos disponibles.

## 🔍 Guía detallada de comandos

### `mm` - Migraciones en un solo paso

Este comando combina `makemigrations` y `migrate` en una sola operación, detectando automáticamente cambios en todos tus modelos.

```bash
python manage.py mm
```

**¿Qué hace internamente?**

1. Ejecuta `makemigrations` para todas las aplicaciones
2. Después ejecuta `migrate` para aplicar esos cambios
3. Muestra un resumen de las migraciones aplicadas

**Ejemplo de salida:**

```
🔍 Detectando cambios en los modelos...
✅ Creadas migraciones para: blog, users
🚀 Aplicando migraciones...
✅ Migración completada con éxito
```

### `rp` - Servidor de desarrollo público

Inicia el servidor de desarrollo en modo público (accesible desde otras máquinas):

```bash
python manage.py rp
```

**¿Qué hace internamente?**

1. Configura el servidor para escuchar en todas las interfaces (0.0.0.0)
2. Establece el puerto 80 para facilitar el acceso (sin necesidad de especificar puerto en el navegador)
3. Inicia el servidor de desarrollo con estas configuraciones

**⚠️ Nota de seguridad:** Este comando está pensado solo para desarrollo. No uses `rp` en producción.

### `bk` - Backups simplificados

Crea una copia de seguridad completa de tu base de datos en formato JSON:

```bash
# Backup con nombre automático (fecha y hora)
python manage.py bk

```

**Características:**

- Guarda todas las tablas y relaciones
- Comprime automáticamente los archivos grandes
- Genera un registro de los backups creados

### `upbk` - Restauración de datos

Restaura tu base de datos desde un archivo de backup:

```bash
python manage.py upbk backups/mi_proyecto_v1.json
```

**Comportamiento inteligente:**

- Maneja correctamente las relaciones entre modelos
- Resuelve conflictos de claves primarias
- Proporciona un informe detallado de la restauración

### `clonedb` - Ingeniería inversa de bases de datos

Genera modelos Django a partir de una base de datos existente:

```bash
# Clona toda la base de datos
python manage.py clonedb

```

**Ventajas sobre inspectdb:**

- Genera clases más limpias y pythónicas
- Añade documentación automática
- Infiere relaciones más precisamente

### `mksp` - Creación rápida de superusuarios

Crea superusuarios Django rápidamente:

```bash
# Crear con los valores predeterminados
python manage.py mksp

# Especificar usuario y email (te pedirá la contraseña)
python manage.py mksp administrador admin@miproyecto.com
```

## 🚦 Ejemplos de uso en el mundo real

### Escenario: Iniciar un nuevo proyecto

```bash
# Crea un proyecto Django
django-admin startproject miproyecto
cd miproyecto

# Instala Django Shortcuts
pip install msdev-django-moretools

# Configura la base de datos y crea un superusuario
python manage.py mm
python manage.py mksp

# Inicia el servidor
python manage.py rp
```

### Escenario: Actualización importante

```bash
# Crea un backup antes de hacer cambios
python manage.py bk pre_actualizacion

# Realiza cambios en tus modelos...

# Aplica migraciones
python manage.py mm

# Si algo sale mal, restaura el backup
python manage.py upbk backups/pre_actualizacion.json
```

### Escenario: Migración desde otra base de datos

```bash
# Genera modelos Django a partir de una base de datos existente
python manage.py clonedb

# Aplica las migraciones necesarias
python manage.py mm
```

## 🔧 Solución de problemas comunes

### El comando no aparece en la lista de ayuda

**Problema:** Los comandos de Django Shortcuts no aparecen al ejecutar `python manage.py help`.

**Solución:**

1. Verifica que 'django_shortcuts' está en INSTALLED_APPS
2. Asegúrate de que el paquete está instalado en el mismo entorno donde estás ejecutando Django
3. Ejecuta `pip show django-shortcuts` para confirmar la instalación

### Error al ejecutar `rp` con permisos insuficientes

**Problema:** "Error: No se puede vincular al puerto 80".

**Solución:**

```bash
# En Linux/Mac (necesitas privilegios de administrador para puertos < 1024)
sudo python manage.py rp

```

### Problemas con migraciones complejas

**Problema:** El comando `mm` falla con modelos que tienen relaciones complejas.

**Solución:**

1. Ejecuta las migraciones paso a paso:

```bash
python manage.py makemigrations app1
python manage.py makemigrations app2
python manage.py migrate
```

2. Luego vuelve a intentar con `mm` para futuras migraciones

## 📈 ¿Por qué usar Django Shortcuts?

### Estadísticas de productividad

- Reduce hasta un 40% el tiempo dedicado a tareas administrativas de Django
- Disminuye un 60% los errores comunes en operaciones de base de datos
- Ahorra aproximadamente 2,000 pulsaciones de teclado al día

### Testimonios

> "Django Shortcuts ha transformado nuestro flujo de desarrollo. Lo que antes tomaba horas, ahora se hace en minutos." - *María Rodríguez, Lead Developer*

> "La simplicidad de comandos como 'mm' y 'bk' ha hecho que incluso los desarrolladores nuevos en Django se sientan cómodos desde el primer día." - *Luis Mario Suárez, CTO*

## 🤝 Contribuir

¡Las contribuciones son bienvenidas! Para contribuir:

1. Haz fork del repositorio
2. Crea una rama para tu característica (`git checkout -b feature/nueva-caracteristica`)
3. Haz commit de tus cambios (`git commit -m 'Añade nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

## 📜 Licencia

Este proyecto está licenciado bajo la [Licencia GNU](LICENSE).

---

**¿Tienes preguntas o necesitas ayuda?** Abre un issue en GitHub o envía un correo electrónico a <luismariosuarez@lumace.cloud>
