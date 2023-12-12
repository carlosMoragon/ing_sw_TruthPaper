if [ -x "$(command -v docker)" ]; then
  echo "Docker ya está instalado en el sistema."
  exit 0
else 
  sudo apt  install docker.io 
fi
sudo docker pull cmoragon/flaskapp:v4

sudo docker run -it -p 4000:4000 -d cmoragon/flaskapp:v4

clear

echo "DISFRUTA DE LAS MEJORES NOTICIAS EN TRUTHPAPER"
echo 
echo "http://127.0.0.1:4000"
