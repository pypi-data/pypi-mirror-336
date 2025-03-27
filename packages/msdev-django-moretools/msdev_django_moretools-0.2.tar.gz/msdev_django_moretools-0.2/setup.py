from setuptools import setup, find_packages

setup(
    name='msdev-django_moretools',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'Django>=5.1.7',
    ],
    author='Luis Mario Cervantes Suárez',
    author_email='luismariosuarez@lumace.cloud',
    description='Paquete de python que contiene las funciones de atajos para Django',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/mariosuarezDEV/django_shortcuts',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
    ],
    python_requires='>=3.12',
)