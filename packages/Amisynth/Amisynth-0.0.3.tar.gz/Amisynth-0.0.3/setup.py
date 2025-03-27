from setuptools import setup, find_packages

setup(
    name='Amisynth',  # Nombre de tu paquete
    version='0.0.3',    # Versión de tu paquete
    packages=find_packages(include=["Amisynth", "Amisynth.*"]),    # Encuentra todas las subcarpetas
    install_requires=["discord.py", "asyncio", "xfox"],  # Dependencias externas si las tienes
    description='Descripción de mi paquete',
    long_description=open('README.md').read(),  # Leer README para información extra
    long_description_content_type='text/markdown',
    author='Amisinth',
    author_email='tuemail@dominio.com',
    url='https://github.com/tu_usuario/mi_paquete',  # Enlace a tu repositorio
    classifiers=[  # Clasificadores para PyPI
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',  # Versión de Python mínima
)
