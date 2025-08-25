# Imagen base oficial de Python 3.10 sobre Debian (Linux)
FROM python:3.10-slim

# Establecer directorio de trabajo
WORKDIR /app

# Establecer PYTHONPATH para que se reconozcan los módulos
ENV PYTHONPATH=/app

# Copiar requirements e instalar dependencias
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copiar el resto del proyecto
COPY . .

# Exponer el puerto de Flask
EXPOSE 5000

# Comando para arrancar con waitress
#CMD ["/bin/bash"]
CMD ["waitress-serve", "--listen=*:5000", "--threads=1", "--channel-timeout=60", "--connection-limit=200", "wsgi:app"]