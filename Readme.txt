JOBBOFFER
├── Proyecto
│   ├── apps
│   ├── joboffers
│   ├── media
│   ├── templates
│   ├── venv
│   └── manage.py
├── scripts_docker
│   └── dev
│       └── run_web.sh
├── docker-compose.override.yml
├── docker-compose.yml
├── Dockerfile
└── requirements.txt

JobOffer/
├── docker-compose.yml
├── docker-compose.override.yml
├── docker-compose.prod.yml
├── Dockerfile
├── requirements.txt
├── Readme.txt
├── certs/                    ← AQUÍ (mismo nivel que docker-compose.yml)
│   ├── cert.pem
│   └── key.pem
├── secrets/
│   └── SECRET_KEY.txt
├── nginx/
│   ├── dev.conf
│   └── prod.conf
├── Proyecto/
├── scripts_docker/


PASO 1: Modificar docker-compose.yml (Configuración COMÚN)
Dónde: docker-compose.yml
Por qué: Necesitamos añadir Nginx como servidor web y crear volúmenes compartidos para archivos estáticos

Cambios:
✏️ Quitar el puerto 80:8000 del servicio web → Solo expondrá el puerto 8000 internamente
➕ Añadir expose: - 8000 → Expone puerto solo para otros contenedores
➕ Añadir volúmenes para archivos estáticos: static_volume y media_volume
➕ Añadir servicio nginx nuevo → Será el servidor web que recibe las peticiones
➕ Definir volúmenes nuevos al final del archivo

PASO 2: Modificar docker-compose.override.yml (DESARROLLO)
Dónde: docker-compose.override.yml
Por qué: Configurar Nginx para desarrollo en puerto 80 sin SSL

Cambios:

➕ Añadir configuración de nginx para desarrollo
➕ Mapear puerto 80:80 → Acceso HTTP simple
➕ Montar archivo de configuración nginx/dev.conf

PASO 3: Modificar docker-compose.prod.yml (PRODUCCIÓN)
Dónde: docker-compose.prod.yml
Por qué: Configurar Nginx para producción con SSL (puerto 443) y redirección HTTPS

Cambios:

✏️ Corregir ruta del comando → De /code/scripts_docker/ a scripts_docker
➕ Añadir configuración de nginx para producción
➕ Mapear puertos 80:80 y 443:443 → HTTP y HTTPS
➕ Montar archivo de configuración nginx/prod.conf
➕ Montar directorio certs con certificados SSL

PASO 4: Crear nginx/dev.conf (NUEVO ARCHIVO)
Dónde: Crear carpeta nginx y archivo nginx/dev.conf
Por qué: Configuración de Nginx para desarrollo

Qué hace:

Escucha en puerto 80 (HTTP simple)
Sirve archivos estáticos desde /code/staticfiles/
Sirve archivos media desde /code/media/
Reenvía peticiones dinámicas a Django (puerto 8000)

PASO 5: Crear nginx/prod.conf (NUEVO ARCHIVO)
Dónde: Crear archivo nginx/prod.conf
Por qué: Configuración de Nginx para producción con SSL

Qué hace:

Redirige puerto 80 → 443 (HTTP → HTTPS)
Escucha en puerto 443 con SSL/TLS
Usa certificados SSL (cert.pem y key.pem)
Sirve archivos estáticos con caché (30 días)
Reenvía peticiones a Django con headers seguros

PASO 6: Modificar run_web.sh
Dónde: run_web.sh
Por qué: El script actual tiene errores (referencia a portfolioDjango)

Cambios:

✏️ Corregir nombre del proyecto → De portfolioDjango a joboffers
➕ Añadir comando collectstatic → Recopila archivos estáticos
➕ Añadir comando migrate → Ejecuta migraciones automáticamente
✏️ Usar Gunicorn correctamente con 3 workers

PASO 7: Modificar settings.py
Dónde: settings.py
Por qué: Configurar correctamente los archivos estáticos para producción

Cambios en la sección STATIC_URL:

➕ Añadir STATIC_ROOT = BASE_DIR / 'staticfiles' → Directorio donde se recopilan estáticos
✏️ Modificar STATICFILES_DIRS → Solo incluir si existe la carpeta static
✅ Mantener STATIC_URL, MEDIA_URL, MEDIA_ROOT

PASO 8: Modificar requirements.txt
Dónde: requirements.txt
Por qué: Necesitamos Gunicorn para producción

Cambios:

➕ Añadir gunicorn==23.0.0 al final del archivo

PASO 9: Crear certificados SSL (PRODUCCIÓN)
Dónde: Crear carpeta certs y generar certificados
Por qué: Necesarios para HTTPS en producción

PASO 10: Verificar carpeta secrets
Dónde: Carpeta secrets con archivo SECRET_KEY.txt
Por qué: Ya existe, solo verificar que tenga contenido
