# Wellcoders: Backend

¡Hola equipo!

Antes de empezar, crearos vuestro propio archivo de settings. La idea es que no vaya en el repositorio porque podrá
contraseñas.

El archivo de docker apunta a `wellcoders_backend/settings_prod.py`.

## Ejecutar el servidor de desarrollo con Docker
En la raíz del proyecto: `docker-compose -f docker-compose-develop.yml up -d`.

## Crear un usuario en django:
En la raíz del proyecto: `docker-compose run wellcoders python manage.py createsuperuser`.

## Despliegue en producción