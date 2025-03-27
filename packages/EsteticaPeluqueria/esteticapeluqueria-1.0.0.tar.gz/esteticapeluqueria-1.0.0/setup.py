from setuptools import setup, find_packages
from pathlib import Path

def read_requirements():
    """Lee los requerimientos del archivo requirements.txt de forma robusta"""
    default_requirements = [
        'PyQt6>=6.4.0',
        'pandas>=2.0.0'
    ]
    
    try:
        with open('requirements.txt', 'r', encoding='utf-8-sig') as f:  # utf-8-sig maneja BOM
            requirements = []
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    if not line[0].isalpha():  # Validar formato
                        print(f"Advertencia: Omite requisito inválido - '{line}'")
                        continue
                    requirements.append(line)
            return requirements if requirements else default_requirements
    except Exception as e:
        print(f"Advertencia: Error leyendo requirements.txt - Usando valores por defecto. Error: {str(e)}")
        return default_requirements

def read_readme():
    """Lee el archivo README.md con manejo de errores"""
    try:
        return Path('README.md').read_text(encoding='utf-8')
    except Exception:
        return "Sistema de Gestión para Estética y Peluquería"

setup(
    name="EsteticaPeluqueria",
    version="1.0.0",
    author="Ugo Gianino",
    author_email="tu@email.com",  # Reemplaza con tu email real
    description="Sistema de gestión para estética y peluquería",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    packages=find_packages(include=['*']),  # Busca todos los paquetes
    package_dir={'': '.'},  # Busca en el directorio raíz
    include_package_data=True,
    package_data={
        '': [
            'data/*.json',
            'views/*.ui',
            'utils/*.qss',
            '*.png',
            '*.ico'
        ],
    },
    install_requires=read_requirements(),
    entry_points={
        'console_scripts': [
            'estetica-pelu=main:main',
        ],
        'gui_scripts': [
            'estetica-pelu-gui=main:main',
        ]
    },
    python_requires='>=3.8',
    license="MIT",
    classifiers=[
    "Development Status :: 4 - Beta",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.8",
    "Programming Language :: Python :: 3.9",
    "Programming Language :: Python :: 3.10",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    "Intended Audience :: End Users/Desktop",
    "Topic :: Office/Business",  # Este es el clasificador válido más cercano
    "Topic :: Utilities",
    ],
    keywords='estetica peluqueria gestion',
    project_urls={
        'Source': 'https://github.com/ugogianino/EsteticaPeluqueria',
        'Bug Reports': 'https://github.com/ugogianino/EsteticaPeluqueria/issues',
    }
)