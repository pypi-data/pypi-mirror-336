from setuptools import setup, find_packages

setup(
    name='amisynth',  # Nombre de tu paquete
    version='0.0.1',  # Versión de tu paquete
    packages=find_packages(),  # Encuentra todas las subcarpetas
    install_requires=["discord.py", "xfox"],  # Dependencias externas si las tienes
    description='Un paquete para integrar funciones personalizadas en Discord',  # Descripción de tu paquete
    long_description=open('README.md').read(),  # Leer README para información extra
    long_description_content_type='text/markdown',
    author='Amisinth',
    author_email='amisynth@gmail.com',  # Tu correo real
    url='https://github.com/tu_usuario/amisynth',  # Enlace a tu repositorio real
    classifiers=[  # Clasificadores para PyPI
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Versión de Python mínima
)
