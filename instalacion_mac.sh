#!/bin/bash

# Verificar si Homebrew está instalado y, si no, instalarlo
if [ ! -x "$(command -v brew)" ]; then
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
fi

# Instalar Docker Desktop usando Homebrew cask
brew install --cask docker

# Iniciar Docker Desktop
open -a Docker

echo "Esperando a que Docker se inicie..."
sleep 10

# Mostrar información sobre la instalación
docker --version
docker-compose --version

echo "La instalación de Docker en macOS se ha completado."

# Descargar la imagen
docker pull cmoragon/flaskapp:v3

# Ejecutar la imagen
docker run -it -p 4000:4000 -d cmoragon/flaskapp:v3

clear

echo "DISFRUTA DE LAS MEJORES NOTICIAS EN TRUTHPAPER"
echo 
echo "http://127.0.0.1:4000"
