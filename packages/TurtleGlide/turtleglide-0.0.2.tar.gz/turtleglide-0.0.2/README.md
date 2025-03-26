TurtleGlide
================

**Introducción**
---------------

TurtleGlide es una herramienta para crear archivos dentro de la carpeta `templates` o `static` de una app de Django.

**Instalación del paquete**
-------------------------

### Instalación en tu proyecto Django

Instalar TurtleGlide en tu proyecto Django:

```bash
pip install TurtleGlide
```

Luego, agregar TurtleGlide como una app de Django en `INSTALLED_APPS`:

```python
INSTALLED_APPS = [
    'TurtleGlide'
]
```

**Uso de TurtleGlide**
---------------------

### Parámetros obligatorios

Hay tres parámetros obligatorios para el uso del comando `create_archive`:

* `app_name`: Nombre de la app
* `file_path`: Ruta del componente HTML
* `--type`: Tipo de archivo a crear:
	+ `template` para archivos en la carpeta `templates`
	+ `static` para archivos en la carpeta `static`

### Comando de ejemplo

```bash
python manage.py create_archive "app_name" "file_path" --type="template"
```

**Instalación para desarrolladores**
---------------------------------

### Paso 1: Instalar dependencias y crear entorno virtual

Llamar al script `setup.sh` para instalar las dependencias y crear el entorno virtual:

```bash
./setup.sh
```

### Paso 2: Activar entorno virtual

Activar el entorno virtual:

```bash
source venv/bin/activate
```

### Listo para empezar

Ya estás listo para empezar a trabajar con TurtleGlide sin problemas.