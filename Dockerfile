FROM python:3.10

# Evita que Python escriba archivos .pyc y muestra logs en tiempo real
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Crea el directorio de trabajo
WORKDIR /code

# Copia e instala dependencias
COPY requirements.txt /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia el código del proyecto Django al contenedor
COPY Proyecto/ /code/

# Expone el puerto 8000 (documentación)
EXPOSE 8000