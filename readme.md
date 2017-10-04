# Wellcoders: Backend

¡Hola equipo!

Antes de empezar, crearos vuestro propio archivo de settings. La idea es que no vaya en el repositorio porque podrá
contraseñas.

El archivo de docker apunta a `wellcoders_backend/settings_prod.py`.

## Ejecutar el servidor de desarrollo con Docker
En la raíz del proyecto: `docker-compose -f docker-compose-develop.yml up -d`.

## Crear un usuario en django:
En la raíz del proyecto: `docker-compose run wellcoders python manage.py createsuperuser`.

## Aceptar cabeceras entre frontend y backend en el entorno de desarrollo
Finalmente está instalada una dependencia en backend para esto, pero como no queremos que esto vaya en producción, introduce en tu settings_prod lo siguiente:
```
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_HEADERS = (
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
)
```