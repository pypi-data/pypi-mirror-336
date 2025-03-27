from setuptools import setup, find_packages
import io

# Leer README con codificación explícita
try:
    with io.open('README.md', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = "Python package containing shortcut functions for Django"

setup(
    name='msdev-django_moretools',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'Django>=5.1.7',
    ],
    author='Luis Mario Cervantes Suarez',  # Removed accents to avoid potential issues
    author_email='luismariosuarez@lumace.cloud',
    description='Python package containing shortcut functions for Django',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/mariosuarezDEV/django_shortcuts',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',  # Corregido el clasificador
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',  # Añadido para mayor claridad
        'Programming Language :: Python :: 3.12',  # Especificando versión compatible
        'Topic :: Internet :: WWW/HTTP',
    ],
    python_requires='>=3.12',
)